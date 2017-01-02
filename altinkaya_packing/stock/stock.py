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
import math


class stock_picking(osv.osv):
    _inherit = "stock.picking"
    _columns = {
        'packing_ids': fields.one2many('delivery.packaging', 'picking_out_id', 'Packing Details'),
        'total_grosswg': fields.float('Total Gross Weight'),
        'total_netwg': fields.float('Total Net Weight'),
        'total_num_pack': fields.integer('Total Packages'),
        'total_volume': fields.float('Total Volume'),
        'total_land': fields.integer('Total Land Weight'),
        'total_air': fields.integer('Total Air Weight'),
    }

#    def _prepare_invoice(self, cr, uid, picking, partner, inv_type, journal_id, context=None):
#        po_id = [picking.id]
#        self.pool.get('stock.picking.out').btn_calc_weight(cr, uid, po_id)
#        invoice_vals = super(stock_picking, self)._prepare_invoice(cr, uid, picking, partner, inv_type, journal_id, context)
#        invoice_vals.update({'address_contact_id': picking.partner_id.id })
#        if picking.packing_ids:
#            picking_ids = []
#            for pick in picking.packing_ids:
#                picking_ids.append(pick.id)
#                invoice_vals.update({'packing_ids': [(6, 0, picking_ids)],
#                                     'carrier_id': picking.carrier_id.id })
#        return invoice_vals

    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, move, context=None):
        inv_vals = super(stock_picking, self)._get_invoice_vals(cr, uid, key, inv_type, journal_id, move,
                                                                context=context)
        sale = move.picking_id.sale_id
        if sale and inv_type in ('out_invoice', 'out_refund'):
            inv_vals.update({
                'comment': sale.note,
                'address_contact_id': move.picking_id.partner_id.id,
            })
        return inv_vals


    def action_invoice_create(self, cr, uid, ids, journal_id=False, group=False, type='out_invoice', context=None):
        res = super(stock_picking, self).action_invoice_create(cr, uid, ids, journal_id, group, type, context)
#        invoice_id = int(res.values()[0])
#        if invoice_id:
#            self.pool.get('account.invoice').btn_calc_weight_inv(cr, uid, [invoice_id])
        return res

    def btn_calc_weight(self, cr, uid, ids, context=None):
        total_g, total_n, total_p = 0, 0, 0
        total_vol = total_air = total_land = 0
        for pick in self.browse(cr, uid, ids[0], context).packing_ids:
            total_g += (pick.grosswg * pick.no_of_cups)
            total_n += (pick.netwg * pick.no_of_cups)
            total_p += pick.no_of_cups
            total_vol += pick.no_of_cups * (((pick.dimension_x * pick.dimension_y * pick.dimension_z) * 1.0) / 1000000)
            total_air += pick.no_of_cups * math.ceil(((pick.dimension_x * pick.dimension_y * pick.dimension_z) * 1.0) / 5000)
            total_land += pick.no_of_cups * math.ceil(((pick.dimension_x * pick.dimension_y * pick.dimension_z) * 1.0) / 3000)
        vals = {
           'total_grosswg': total_g,
           'total_netwg': total_n,
           'total_num_pack': total_p,
           'total_volume': total_vol,
           'total_air': total_air,
           'total_land': total_land,
        }
        self.write(cr, uid, ids, vals, context)
        return True

stock_picking()

class delivery_packaging(osv.osv):
    _name = "delivery.packaging"
    _columns = {
        'pack_no': fields.integer('Pack Number'),
        'dimension_x': fields.integer('Pack Width'),
        'dimension_y': fields.integer('Pack Length'),
        'dimension_z': fields.integer('Pack Height'),
        'no_of_cups': fields.integer('Number of Cups'),
        'picking_out_id': fields.many2one('stock.picking', 'Picking Out', invisible=True),
        'invoice_id': fields.many2one('account.invoice', 'Invoice', readonly=True),
        'grosswg': fields.float('Gross Weight'),
        'netwg': fields.float('Net Weight'),
    }
delivery_packaging()
