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

from openerp.osv import fields
from openerp.osv import osv
from openerp.tools.translate import _


class sale_order(osv.osv):
    _inherit = 'sale.order'

    def send_fax(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        sendfax_obj = self.pool.get('faxsend.queue')
        faxacc_obj = self.pool.get('faxsend.account')
        faxacc_id = faxacc_obj.search(cr, uid, [])
        if not faxacc_id:
            raise osv.except_osv(_('Error'),
                                 _('Please configure fax account'))
        for sale in self.browse(cr, uid, ids):
            if not sale.partner_id.fax:
                raise osv.except_osv(_('Error'),
                                     _('Customer has no faxno'))
            fax_val = {
                'report': 'sale.order',
                'faxno': sale.partner_id.fax,
                'object_type': 'report',
                'obj_id': sale.id,
                'subject': sale.name,
                'account_id': faxacc_id[0],
                'state': 'wait',
            }
            fax_id = sendfax_obj.create(cr, uid, fax_val)
            sendfax_obj.process_faxes(cr, uid, [fax_id], context=context)
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: