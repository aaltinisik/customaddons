from openerp import models
from openerp import fields
from openerp import api

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    date_export = fields.Date(string="Export Date")
    amount_total_tl = fields.Float(string='Amount Total TRY',
                                    compute='_compute_amount_tl',
                                    store=False)
    amount_untaxed_tl = fields.Float(string='Amount Untaxed TRY',
                                   compute='_compute_amount_tl',
                                   store=False)
    amount_tax_tl = fields.Float(string='Amount tax TRY',
                                     compute='_compute_amount_tl',
                                     store=False)

    @api.one
    @api.depends('currency_id', 'amount_total', 'date_export', 'date_invoice')
    def _compute_amount_tl(self):
        cr, uid, context = self._cr, self._uid, self._context
        if context is None:
            context = {}
        currency_obj = self.pool.get('res.currency')
        currency_try = self.env['res.currency'].search([('name', '=', 'TRY')])
        ctx = context.copy()
        ctx['date'] = self.date_export or self.date_invoice
        self.amount_total_tl = currency_obj.compute(cr, uid, self.currency_id.id, currency_try.id,
                                                    self.amount_total, context=ctx)
        self.amount_tax_tl = currency_obj.compute(cr, uid, self.currency_id.id, currency_try.id,
                                                    self.amount_tax, context=ctx)
        self.amount_untaxed_tl = currency_obj.compute(cr, uid, self.currency_id.id, currency_try.id,
                                                    self.amount_untaxed, context=ctx)
