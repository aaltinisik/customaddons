# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import float_is_zero, float_compare


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    currency_difference_checked = fields.Boolean(string='Currency Difference Checked', default=False,
                                            compute='_compute_currency_difference_checked', store=False)
    currency_difference_amount = fields.Monetary(string='Currency Difference Amount')

    @api.depends('currency_difference_amount')
    def _compute_currency_difference_checked(self):
        prec = self.env['decimal.precision'].precision_get('Account')
        for line in self:
            if float_compare(line.currency_difference_amount, abs(line.amount_currency), precision_digits=prec):
                line.currency_difference_checked = False
            else:
                line.currency_difference_checked = True

    # def create(self, vals):
    #     res = super(AccountMoveLine, self).create(vals)
    #     for line in res:
    #         line.amount_currency = line._calculate_amount_currency()
    #     return res
    #
    # def _calculate_amount_currency(self):
    #     prec = self.env['decimal.precision'].precision_get('Account')
    #     for line in self:
    #         partner_currency_id = line.partner_id.secondary_curr_id
    #         if float_is_zero(line.amount_currency, prec) and partner_currency_id:
    #             amount = line.amount_residual or 0.0
    #             currency_id = line.currency_id or line.company_id.currency_id
    #             return currency_id._convert(amount, partner_currency_id, line.company_id, line.date,
    #                                                         round=False)
    #         return line.amount_currency
