# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today Acespritech Solutions Pvt Ltd
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    total_balance = fields.Float(string='Total Balance', readonly=True)

    @api.multi
    @api.depends('partner_id')
    def partner_balance(self, partner_id):
        partner = self.env['res.partner'].browse(partner_id)
        balance = 0
        if partner.parent_id:
            balance = partner.parent_id.credit - partner.parent_id.debit
        else:
            balance = partner.credit - partner.debit
        return balance

    @api.model
    def create(self, vals):
        if vals.get('partner_id'):
            vals['total_balance'] = self.partner_balance(vals['partner_id'])
        return super(AccountInvoice, self).create( vals)

    def write(self,vals):
        for invoice in self:
            partner_id = False
            if vals.get('partner_id'):
                partner_id = vals['partner_id']
            else:
                partner_id = invoice.partner_id.id
            vals['total_balance'] = self.partner_balance(partner_id)
        return super(AccountInvoice, self).write( vals)

