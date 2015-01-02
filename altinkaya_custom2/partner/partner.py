# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2013-Present Acespritech Solutions Pvt. Ltd. (<http://acespritech.com>).
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
from openerp.osv import osv, fields
from openerp.tools.translate import _


class res_partner(osv.osv):
    _inherit = "res.partner"

    _columns = {
    'z_old_tel': fields.char('Eski Tel', size=64, required=False),
    'z_old_fax': fields.char('Eski Faks', size=64, required=False),
    'z_old_cep': fields.char('Eski Faks', size=64, required=False),

    }


    def create_accounts(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        account_obj = self.pool.get('account.account')
        aat_obj = self.pool.get('account.account.type')
        imd_obj = self.pool.get('ir.model.data')
        rec_type = aat_obj.search(cr, uid, [('code', '=', 'receivable')])
        pay_type = aat_obj.search(cr, uid, [('code', '=', 'payable')])
        for partner in self.browse(cr, uid, ids):
            if not partner.ref:
                raise osv.except_osv(_('No Reference!'),
                                     _("You must define reference for creating accounts!"))
            code = '120.' + (partner.ref and str(partner.ref).strip() or '')
            code_pay = '320.' + (partner.ref and str(partner.ref).strip() or '')
            acc_rec_id = account_obj.search(cr, uid, [('code', '=', code)])
            acc_pay_id = account_obj.search(cr, uid, [('code', '=', code_pay)])
            if acc_rec_id:
                raise osv.except_osv(_('Account Exist!'),
                                     _("Account Receivable is already created with this reference."))
            if acc_pay_id:
                raise osv.except_osv(_('Account Exist!'),
                                     _("Account Payable is already created with this reference."))
            parent_rec_id = imd_obj.get_object_reference(cr, uid, 'account', 'conf_a_recv')[1]
            parent_cre_id = imd_obj.get_object_reference(cr, uid, 'account', 'conf_a_pay')[1]
            acc_rec_data = {
               'code': code,
               'name': partner.name,
               'parent_id': parent_rec_id,
               'reconcile':True,
               'type':'receivable',
               'user_type': rec_type and rec_type[0] or False
            }
            acc_recievable = account_obj.create(cr, uid, acc_rec_data)
            acc_pay_data = {
                'code': code_pay,
                'name': partner.name,
                'parent_id': parent_cre_id,
                'reconcile':True,
                'type':'payable',
                'user_type': pay_type and pay_type[0] or False
            }
            acc_payable = account_obj.create(cr, uid, acc_pay_data)
            self.write(cr, uid, partner.id, {'property_account_receivable': acc_recievable,
                                             'property_account_payable': acc_payable})
        return True

res_partner()
