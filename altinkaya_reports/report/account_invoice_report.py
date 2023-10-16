from odoo import models, fields, api, tools


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    usd_rate = fields.Float('USD Rate', compute='_compute_usd_rate', store=True, default=1.0)

    @api.multi
    @api.depends('date_invoice', 'currency_id')
    def _compute_usd_rate(self):
        currency_usd = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        for ai in self:
            date_invoice = ai.date_invoice
            try:
                ai.currency_rate = ai.currency_id.with_context(date=date_invoice).rate or 1.0
                ai.usd_rate = currency_usd.with_context(date=date_invoice).rate or 1.0
            except Exception:
                pass

class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    state_id = fields.Many2one('res.country.state', string='State', readonly=True)
    price_total_usd = fields.Float(string='Untaxed Total USD', readonly=True)
    total_tax = fields.Float(string='Tax Total', readonly=True)
    price_average_usd = fields.Float(string='Average Price USD', readonly=True, group_operator="avg")
    source_id = fields.Many2one('utm.source', string='Marketing Source', readonly=True)
    campaign_id = fields.Many2one('utm.campaign', string='Marketing Campaign', readonly=True)
    month_nr = fields.Char('Ay No', readonly=True)

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + \
               ", sub.state_id, sub.total_tax as total_tax, sub.price_total_usd as price_total_usd, sub.price_average_usd as price_average_usd, sub.source_id as source_id, sub.campaign_id as campaign_id, sub.month_nr as month_nr"

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select() + \
               """, coalesce(partner.state_id, partner_ai.state_id) AS state_id,
               partner.source_id,partner.campaign_id,
               to_char(ai.date_invoice, 'MM') AS month_nr,
               SUM(ail.price_subtotal_signed * invoice_type.sign * ai.usd_rate) AS price_total_usd,
               SUM(
                   CASE 
                       WHEN aa.code LIKE '191.0%' THEN -ait.amount_total_currency 
                       WHEN aa.code LIKE '391.0%'  THEN ait.amount_total_currency 
                       ELSE 0
                   END
               ) / NULLIF(COUNT(*) OVER (PARTITION BY ai.id), 0) AS total_tax,
               sum(abs(ail.price_subtotal_signed) * ai.usd_rate) /
                CASE
                    WHEN sum(ail.quantity / COALESCE(u.factor, 1::numeric) * COALESCE(u2.factor, 1::numeric)) <> 0::numeric THEN sum(ail.quantity / COALESCE(u.factor, 1::numeric) * COALESCE(u2.factor, 1::numeric))
                    ELSE 1::numeric
                END AS price_average_usd"""

    def _from(self):
        return super(AccountInvoiceReport, self)._from() + \
                  """
                  LEFT JOIN account_invoice_tax ait ON ai.id = ait.invoice_id
                  LEFT JOIN account_account aa ON ait.account_id = aa.id
                  """

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + ", coalesce(partner.state_id, partner_ai.state_id),partner.source_id,partner.campaign_id,month_nr"

