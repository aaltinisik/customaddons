# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    has_secondary_curr = fields.Boolean(string='Has secondary currency?', default=False)
    secondary_curr_id = fields.Many2one('res.currency', string='Currency')

    def calc_difference_invoice(self):
        prec = self.env['decimal.precision'].precision_get('Account')
        for partner in self:
            if partner.has_secondary_curr:
                lines = self.env['account.move.line'].search([('partner_id', '=', partner.id), ('invoice_id', '!=', False)])
                for line in lines:
                    payment = line.credit or line.debit
                    amount_currency = round(abs(line.amount_currency or line._calculate_amount_currency()), prec)
