from openerp import models, fields, api, _
import datetime

# from openerp.osv import fields, osv


class account_invoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('currency_id', 'amount_total', 'date_export', 'date_invoice')
    def _compute_amounts_in_try_currency(self):
        cr, uid, ids, context = self._cr, self._uid, self._ids, self._context
        if context is None:
            context={}
        currency_obj = self.pool.get('res.currency')
        currency_rate_obj = self.pool.get('res.currency.rate')
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        user_currency_id = user.company_id.currency_id.id
        date_val = self.date_export or self.date_invoice
        if date_val and self.currency_id:
            try_cur_id = currency_obj.search(cr, uid, [('name', '=', 'TRY')], limit=1, context=context)
            if try_cur_id and try_cur_id[0] != user_currency_id:
                currency_rate_id = currency_rate_obj.search(cr, uid, [
                        ('name', '>=', date_val + " 00:00:00"),
                        ('name', '<', date_val + " 23:59:59"),
    #                     ('currency_id.company_id', '=', user.company_id.id),
                        ('currency_id', '=', try_cur_id[0])
                        ], limit=1, context=context)
                if currency_rate_id:
                    currency_rate_id = currency_rate_id[0]
                    base_currency_id = currency_rate_obj.browse(cr, uid, currency_rate_id, context=context).currency_id.id
                    ctx = context.copy()
                    ctx['date'] = self.date_export or self.date_invoice
                    price_total = currency_obj.compute(cr, uid, user_currency_id, base_currency_id, self.amount_total, context=ctx)
                    self.amount_total_try = price_total
            else:
                self.amount_total_try = self.amount_total

    date_export = fields.Date(string="Date Export")
    amount_total_try = fields.Float(string="Amount Total TRY", compute='_compute_amounts_in_try_currency', store=False)

