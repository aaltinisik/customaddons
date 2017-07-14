from openerp import models, fields, api, _
import datetime

# from openerp.osv import fields, osv


class account_invoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('currency_id', 'amount_total', 'date_export', 'date_invoice')
    def check_amount_total(self):
        if self.currency_id.name == 'TRY':
            self.amount_total_try = self.amount_total
        else:
            export_date = self.date_export if self.date_export else self.date_invoice
            if export_date:
                record_id = self.env['res.currency.rate'].search([('currency_id.name', '=', 'TRY'), ('name', '=', export_date)], order='id desc', limit=1)
                if record_id:
                    self.amount_total_try = self.amount_total * record_id.rate

#     def check_amount_total(self, cr, uid, ids, field_name, arg, context=None):
#         invoice_id = self.browse(cr, uid, ids)
#         if invoice_id:
#             if invoice_id.currency_id.name == 'TRY':
#                 invoice_id.amount_total_try = 1500
#             else:
#                 invoice_id.amount_total_try = 0.0

    date_export = fields.Date(string="Date Export")
    amount_total_try = fields.Float(string="Amount Total TRY", compute='check_amount_total', store=True)

#     _columns = {
#         'date_export': fields.date('Date Export'),
#         'amount_total_try': fields.function(check_amount_total, string='Amount Total Try', type='float', store=True)
#      }
