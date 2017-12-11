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


class product_product(osv.osv):
    _inherit = "product.product"

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        product_id = super(product_product, self).create(cr, uid, vals, context=context)
        if vals.get('type') == 'product':
            warehouse_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'stock', 'warehouse0')[1]
            warehouse = self.pool.get('stock.warehouse').browse(cr, uid, warehouse_id)
            #product_search_data = self.pool.get('product.product').search(cr,uid,[('product_tmpl_id','=',product_id)],context=context)
            #product_browse_data = self.pool.get('product.product').browse(cr,uid,product_search_data,context)
            self.pool.get('stock.warehouse.orderpoint').create(cr, uid,
                                            {'product_id': product_id,
                                            'product_max_qty': 0,
                                            'product_min_qty': 0,
                                            'qty_multiple': 1,
                                            'location_id': warehouse.lot_stock_id.id,
                                            'warehouse_id': warehouse_id,
                                            'product_uom': vals.get('uom_id')})
        return product_id

product_product()
