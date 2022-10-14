# -*- encoding: utf-8 -*-


from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    x_cek_vergi = fields.Char('Cek Vergi No', size=64)
    x_cek_tarih = fields.Date('Keside Tarihi', help="Cekin Vade Tarihi")
    x_cek_no = fields.Char('Cek No', size=64)
    x_cek_banka = fields.Char('Cek banka Adi', size=64)
    date_due = fields.Date('Date Due')

    statement_line_id = fields.Many2one('account.bank.statement.line', 'Bank Statement Line')
