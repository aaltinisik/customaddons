from odoo import models, fields, api
from datetime import datetime


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
        currency_obj = self.env['res.currency'].browse(self.currency_id.id)
        currency_try = self.env['res.currency'].search([('name', '=', 'TRY')], limit=1)
        company = self.env['res.company'].browse(1)
        date = self.date_export or self.date_invoice or datetime.now()
        self.amount_total_tl = currency_obj._convert(self.amount_total, currency_try, company, date)
        self.amount_tax_tl = currency_obj._convert(self.amount_tax, currency_try, company, date)
        self.amount_untaxed_tl = currency_obj._convert(self.amount_untaxed, currency_try, company, date)
