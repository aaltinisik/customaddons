from openerp import models
from openerp import fields
from openerp import api

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('currency_id', 'amount_total', 'date_export', 'date_invoice')
    def check_amount_total(self):
        currency_obj = self.pool.get('res.currency')
        currency_rate_obj = self.pool.get('res.currency.rate')
        invoice_currency_id = self.currency_id
        if invoice_currency_id.name == 'TRY':
            self.amount_total_try = self.amount_total
        else:
            self.amount_total_try = self.amount_total
            return True
            export_date = self.date_export if self.date_export else self.date_invoice
            if export_date:
                record_id = self.env['res.currency.rate'].search([('currency_id.name', '=', 'TRY'), ('name', '=', export_date)], order='id desc', limit=1)
                if record_id:
                    self.amount_total_try = self.amount_total * record_id.rate

    date_export = fields.Date(string="Export Date")
    amount_total_try = fields.Float(string="Amount Total TRY", compute='check_amount_total', store=False)

#     _columns = {
#         'date_export': fields.date('Date Export'),
#         'amount_total_try': fields.function(check_amount_total, string='Amount Total Try', type='float', store=True)
#      }
