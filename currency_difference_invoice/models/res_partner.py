# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.tools import float_is_zero, float_compare

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    has_secondary_curr = fields.Boolean(string='Has secondary currency?', default=False)
    secondary_curr_id = fields.Many2one('res.currency', string='Currency')

    def calc_difference_invoice(self):
        prec = self.env['decimal.precision'].precision_get('Account')
        if self.has_secondary_curr:

            invoices_domain = [('state', '=', 'open'), ('type', '=', 'out_invoice'), ('partner_id', '=', self.id)]
            lines_domain = [('partner_id', '=', self.id), ('invoice_id', '!=', False)]

            invoices = self.env['account.invoice'].search(invoices_domain)
            lines = self.env['account.move.line'].search(lines_domain)
            onhand_credit = 0.0
            next_index = -1
            for invoice in invoices:
                total = invoice.amount_total - onhand_credit
                if total > 0:
                    for index, line in enumerate(lines[next_index+1:]):
                        total -= (round(line.amount_currency or line._calculate_amount_currency(), prec)
                                  + onhand_credit)
                        if float_compare(total, 0.0, precision_digits=prec) == -1 or 0:
                            onhand_credit += abs(total)
                            next_index += index
                            break

                    lines[:next_index + 1].write({'is_difference_invoice': True})



            # for line in lines:
            #     payment = line.credit or line.debit
            #     amount_currency = round(abs(line.amount_currency or line._calculate_amount_currency()), prec)
