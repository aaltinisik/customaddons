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
import time
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class stock_picking(osv.osv):
    _inherit = "stock.picking"
    _columns = {
        'packing_tracking_ids': fields.one2many('stock.tracking', 'picking_out_id', 'Packing Details'),
        'total_grosswg': fields.float('Total Gross Weight'),
        'total_netwg': fields.float('Total Net Weight'),
        'total_num_pack': fields.integer('Total Packages'),
        'total_volume': fields.float('Total Volume'),
        'total_land': fields.integer('Total Land Weight'),
        'total_air': fields.integer('Total Air Weight'),
    }

    def _prepare_invoice(self, cr, uid, picking, partner, inv_type, journal_id, context=None):
        po_id = [picking.id]
        self.pool.get('stock.picking').btn_calc_weight(cr, uid, po_id)
        invoice_vals = super(stock_picking, self)._prepare_invoice(cr, uid, picking, partner, inv_type, journal_id, context) 
        invoice_tracking_ids = []
        for pack in picking.packing_tracking_ids:
            if pack.id:
                invoice_tracking_ids.append(pack.id)
        invoice_vals.update({'packing_tracking_ids': [(6, 0, invoice_tracking_ids)],
                             'carrier_id': picking.carrier_id.id,
                             'address_contact_id': picking.partner_id.id,
                             })
        return invoice_vals

    def action_invoice_create(self, cr, uid, ids, journal_id=False, group=False, type='out_invoice', context=None):
        res = super(stock_picking, self).action_invoice_create(cr, uid, ids, journal_id, group, type, context)
        invoice_id = int(res.values()[0])
#        if invoice_id:
#            self.pool.get('account.invoice').btn_calc_weight_inv(cr, uid, [invoice_id])
        return res

    def btn_print_pack(self, cr, uid, ids, context=None):
        self.btn_calc_weight(cr, uid, ids, context)

        for pack in self.browse(cr, uid, ids[0], context).packing_tracking_ids:
            denemepackname=pack.name
            denemeids=pack.move_ids
            for move in pack.move_ids:
                produename = move.product_id.name
                produeqty = move.product_qty

        return True

    def btn_calc_weight(self, cr, uid, ids, context=None):
        total_g, total_n, total_p = 0, 0, 0
        total_vol = total_air = total_land = 0

        tracking_ids = []
        for move in self.browse(cr, uid, ids[0], context).move_lines:
            if move.tracking_id.id:
                if move.tracking_id.id not in tracking_ids:
                    tracking_ids.append(move.tracking_id.id)
                    total_g += move.tracking_id.gross_weight
                    total_n += move.tracking_id.net_weight
                    total_p += 1
                    total_vol += (((move.tracking_id.pack_h * move.tracking_id.pack_w * move.tracking_id.pack_l) * 1.0) / 1000000)
                    total_air += math.ceil(((move.tracking_id.pack_h * move.tracking_id.pack_h * move.tracking_id.pack_h) * 1.0) / 5000)
                    total_land += math.ceil(((move.tracking_id.pack_h * move.tracking_id.pack_h * move.tracking_id.pack_h) * 1.0) / 3000)
        vals = {
           'packing_tracking_ids': [(6, 0, tracking_ids)],
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
class stock_production_lot(osv.osv):
    _inherit = 'stock.production.lot'

    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        reads = self.read(cr, uid, ids, ['name', 'prefix', 'ref'], context)
        res = []
        for record in reads:
            name = record['name']
            prefix = record['prefix']
            if prefix:
                name = prefix + '/' + name
            if record['ref']:
                name = '%s [%s]' % (name, record['ref'])
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        args = args or []
        ids = []
        if name:
            ids = self.search(cr, uid, [('prefix', '=', name)] + args, limit=limit, context=context)
            if not ids:
                ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)

    def _get_stock(self, cr, uid, ids, field_name, arg, context=None):
        """ Gets stock of products for locations
        @return: Dictionary of values
        """
        if context is None:
            context = {}
        if 'location_id' not in context:
            locations = self.pool.get('stock.location').search(cr, uid, [('usage', '=', 'internal')], context=context)
        else:
            locations = context['location_id'] and [context['location_id']] or []

        if isinstance(ids, (int, long)):
            ids = [ids]

        res = {}.fromkeys(ids, 0.0)
        if locations:
            cr.execute('''select
                    prodlot_id,
                    sum(qty)
                from
                    stock_report_prodlots
                where
                    location_id IN %s and prodlot_id IN %s group by prodlot_id''',(tuple(locations),tuple(ids),))
            res.update(dict(cr.fetchall()))

        return res

    def _stock_search(self, cr, uid, obj, name, args, context=None):
        """ Searches Ids of products
        @return: Ids of locations
        """
        locations = self.pool.get('stock.location').search(cr, uid, [('usage', '=', 'internal')])
        cr.execute('''select
                prodlot_id,
                sum(qty)
            from
                stock_report_prodlots
            where
                location_id IN %s group by prodlot_id
            having  sum(qty) '''+ str(args[0][1]) + str(args[0][2]),(tuple(locations),))
        res = cr.fetchall()
        ids = [('id', 'in', map(lambda x: x[0], res))]
        return ids
    _columns = {
        'stock_available': fields.function(_get_stock, fnct_search=_stock_search, type="float", string="Available", select=True,
            help="Current quantity of products with this Serial Number available in company warehouses",
            digits_compute=dp.get_precision('Product Unit of Measure')),
        'prefix': fields.char('Prefix', size=64, help="Optional prefix to prepend when displaying this serial number: PREFIX/SERIAL [INT_REF]"),
       # 'move_ids': fields.one2many('stock.move', 'prodlot_id', 'Moves for this serial number', readonly=True),
    }

class stock_move(osv.osv):
    _inherit = 'stock.move'

    _columns = {
        'tracking_id': fields.many2one('stock.tracking', 'Pack', select=True, states={'done': [('readonly', True)]}, help="Logistical shipping unit: pallet, box, pack ..."),
       # 'prodlot_id': fields.many2one('stock.production.lot', 'Serial Number', help="Serial number is used to put a serial number on the production", select=True, ondelete='restrict'),
    }

    def onchange_lot_id(self, cr, uid, ids, prodlot_id=False, product_qty=False,
                        loc_id=False, product_id=False, uom_id=False, context=None):
        """ On change of production lot gives a warning message.
        @param prodlot_id: Changed production lot id
        @param product_qty: Quantity of product
        @param loc_id: Location id
        @param product_id: Product id
        @return: Warning message
        """
        if not prodlot_id or not loc_id:
            return {}
        ctx = context and context.copy() or {}
        ctx['location_id'] = loc_id
        ctx.update({'raise-exception': True})
        uom_obj = self.pool.get('product.uom')
        product_obj = self.pool.get('product.product')
        product_uom = product_obj.browse(cr, uid, product_id, context=ctx).uom_id
        prodlot = self.pool.get('stock.production.lot').browse(cr, uid, prodlot_id, context=ctx)
        location = self.pool.get('stock.location').browse(cr, uid, loc_id, context=ctx)
        uom = uom_obj.browse(cr, uid, uom_id, context=ctx)
        amount_actual = uom_obj._compute_qty_obj(cr, uid, product_uom, prodlot.stock_available, uom, context=ctx)
        warning = {}
        if (location.usage == 'internal') and (product_qty > (amount_actual or 0.0)):
            warning = {
                'title': _('Insufficient Stock for Serial Number !'),
                'message': _('You are moving %.2f %s but only %.2f %s available for this serial number.') % (product_qty, uom.name, amount_actual, uom.name)
            }
        return {'warning': warning}

class stock_tracking(osv.osv):
    _name = "stock.tracking"
    _description = "Packs"

    def checksum(sscc):
        salt = '31' * 8 + '3'
        sum = 0
        for sscc_part, salt_part in zip(sscc, salt):
            sum += int(sscc_part) * int(salt_part)
        return (10 - (sum % 10)) % 10
    checksum = staticmethod(checksum)

    def make_sscc(self, cr, uid, context=None):
        sequence = self.pool.get('ir.sequence').get(cr, uid, 'stock.lot.tracking')
        try:
            return sequence + str(self.checksum(sequence))
        except Exception:
            return sequence
    def _get_net_weight(self, cr, uid, ids, field_name, arg=None, context=None):
        res = {}
        for pack in self.browse(cr, uid, ids, context=context):
            res[pack.id] = pack.gross_weight - pack.pack_tare
        return res
    def _get_cbm(self, cr, uid, ids, fields, arg=None,  context=None):
        res = {}
        for pack in self.browse(cr, uid, ids, context=context):
            cbm = pack.pack_h * pack.pack_l * pack.pack_w
            cbm = cbm != 0 and cbm/1000000.0
            res[pack.id] = cbm
        return res

    _columns = {
        'name': fields.char('Pack Reference', size=64, required=True, select=True, help="By default, the pack reference is generated following the sscc standard. (Serial number + 1 check digit)"),
        'active': fields.boolean('Active', help="By unchecking the active field, you may hide a pack without deleting it."),
        'serial': fields.char('Additional Reference', size=64, select=True, help="Other reference or serial number"),
        'move_ids': fields.one2many('stock.move', 'tracking_id', 'Moves for this pack', readonly=True),
        'date': fields.datetime('Creation Date', required=True),
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
    _defaults = {
        'active': 1,
        'name': make_sscc,
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        ids = self.search(cr, user, [('serial', '=', name)]+ args, limit=limit, context=context)
        ids += self.search(cr, user, [('name', operator, name)]+ args, limit=limit, context=context)
        return self.name_get(cr, user, ids, context)

    def name_get(self, cr, uid, ids, context=None):
        """Append the serial to the name"""
        if not len(ids):
            return []
        res = [ (r['id'], r['serial'] and '%s [%s]' % (r['name'], r['serial'])
                                      or r['name'] )
                for r in self.read(cr, uid, ids, ['name', 'serial'],
                                   context=context) ]
        return res

    def unlink(self, cr, uid, ids, context=None):
        raise osv.except_osv(_('Error!'), _('You cannot remove a lot line.'))

    def action_traceability(self, cr, uid, ids, context=None):
        """ It traces the information of a product
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: List of IDs selected
        @param context: A standard dictionary
        @return: A dictionary of values
        """
        return self.pool.get('action.traceability').action_traceability(cr,uid,ids,context)

stock_tracking()
