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
from openerp.osv import fields, osv, orm
import openerp.addons.decimal_precision as dp


class account_invoice(osv.osv):
    _inherit = 'account.invoice'
    _columns = {
        'total_balance': fields.float(string='Total Balance', readonly=True),
    }

    def partner_balance(self, cr, uid, partner_id, context=None):
        if context is None:
            context = {}
        partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
        balance = 0
        if partner.parent_id:
            balance = partner.parent_id.credit - partner.parent_id.debit
        else:
            balance = partner.credit - partner.debit
        return balance

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('partner_id'):
            vals['total_balance'] = self.partner_balance(cr, uid, vals['partner_id'])
        return super(account_invoice, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        for invoice in self.browse(cr, uid, ids, context):
            partner_id = False
            if vals.get('partner_id'):
                partner_id = vals['partner_id']
            else:
                partner_id = invoice.partner_id.id
            vals['total_balance'] = self.partner_balance(cr, uid, partner_id)
        return super(account_invoice, self).write(cr, uid, ids, vals, context=context)

account_invoice()
