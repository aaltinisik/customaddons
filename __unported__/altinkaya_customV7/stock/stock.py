# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2012-Present (<http://www.acespritech.com/>) Acespritech Solutions Pvt.Ltd
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


class stock_picking_out(osv.osv):
    _inherit = "stock.picking.out"

    def open_sales_order(self, cr, user, ids, context=None):
        delivery_datas = self.browse(cr, user, ids[0])
        sale_order_id = delivery_datas.sale_id and delivery_datas.sale_id.id
        view_id = self.pool.get('ir.model.data').get_object_reference(cr, user, 'sale', 'view_order_form')[1]
        return {
            'res_id':sale_order_id,
            'view_id':[view_id],
            'view_type':'form',
            'view_mode':'form',
            'res_model':'sale.order',
            'type':'ir.actions.act_window',
            'target':'current',
        }
stock_picking_out()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
