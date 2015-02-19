# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2010-2013 Elico Corp. All Rights Reserved.
#     Jon Chow <jon.chow@elico-corp.com>
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

from openerp.osv import fields, osv


class  stock_tracking(osv.osv):
    _inherit ='stock.tracking'
    def _get_net_weight(self, cr, uid, ids, field_name, arg=None, context=None):
        res = {}
        for pack in self.browse(cr, uid, ids, context=context):
            res[pack.id] = pack.gross_weight - pack.pack_tare
        return res
    def _get_cbm(self, cr, uid, ids, fields, arg=None,  context=None):
        res = {}
        for ul in self.browse(cr, uid, ids, context=context):
            cbm = ul.high * ul.width * ul.long
            cbm = cbm != 0 and cbm/1000000
            res[ul.id] = cbm
        return res

    _columns={
        'pack_lineorder': fields.integer('Pack order in shipment'),
        'picking_out_id': fields.many2one('stock.picking.out', 'Picking Out'),
        'invoice_id': fields.many2one('account.invoice', 'Invoice'),
        'ul_id':    fields.many2one('product.ul','Pack Template'),
        'pack_h':   fields.float('H (cm)', digits=(3,3)),
        'pack_w':   fields.float('W (cm)', digits=(3,3)),
        'pack_l':   fields.float('L (cm)', digits=(3,3)),
        'pack_cbm': fields.function(_get_cbm, arg=None, type='float', digits=(3,3), string='CBM'),
        'pack_tare': fields.float('Tare Kg', digits=(3,3)),

        'pack_address': fields.char('Address', size=128),
        'pack_note':    fields.char('Note', size=128),

        'gross_weight': fields.float('GW (Kg)'),
        'net_weight':   fields.function(_get_net_weight, arg=None, type='float', string='Net (Kg)'),
    }



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: