# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import float_is_zero

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    is_difference_invoice = fields.Boolean(string='Is Difference Invoice')
    difference_amount = fields.Monetary(string='Difference Amount')

    def create(self, vals):
        res = super(AccountMoveLine, self).create(vals)
        res.amount_currency = res._calculate_amount_currency()
        return res

    def _calculate_amount_currency(self):
        prec = self.env['decimal.precision'].precision_get('Account')
        for line in self:
            partner_currency_id = line.partner_id.secondary_curr_id
            if float_is_zero(line.amount_currency, prec) and partner_currency_id:
                amount = line.credit or line.debit or 0.0
                currency_id = line.currency_id or line.company_id.currency_id
                return currency_id._convert(amount, partner_currency_id, line.company_id, line.date,
                                                            round=False)
            return line.amount_currency
