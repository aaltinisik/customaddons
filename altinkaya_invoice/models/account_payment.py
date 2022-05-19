# -*- encoding: utf-8 -*-


from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    x_cek_vergi = fields.Char('Cek Vergi No', size=64)
    x_cek_tarih = fields.Date('Keside Tarihi', help="Cekin Vade Tarihi")
    x_cek_no = fields.Char('Cek No', size=64)
    x_cek_banka = fields.Char('Cek banka Adi', size=64)
    date_due = fields.Date('Date Due')
    amount_in_try = fields.Monetary(string='Amount In TRY', store=True,
                                    readonly=True, compute='_compute_amount_in_try')

    def _compute_amount_in_try(self):
        for rec in self:
            if rec.currency_id != rec.company_id.currency_id:
                rec.amount_in_try = rec.currency_id._convert(
                    rec.amount, rec.company_id.currency_id, rec.company_id, rec.payment_date)
            else:
                rec.amount_in_try = rec.amount
