# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    currency_difference_checked = fields.Boolean(string='Currency Difference Checked', default=False)

    def create(self, vals):
        if vals.get('currency_id', False) and vals.get('partner_id', False):
            currency = self.env['res.currency'].browse(vals['currency_id'])
            partner = self.env['res.partner'].browse(vals['partner_id'])
            if currency != partner.currency_id:
                raise ValidationError(_('The currency of the invoice must be the same as the currency of the partner.'))
        return super(AccountInvoice, self).create(vals)
