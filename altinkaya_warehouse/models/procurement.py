# -*- encoding: utf-8 -*-
#
#Created on Jan 23, 2019
#
#@author: dogan
#
from openerp import models, api, fields
from openerp import SUPERUSER_ID

class ProcurementOrder(models.Model):
    _inherit = "procurement.order"

    @api.model
    def _prepare_orderpoint_procurement(self, orderpoint, product_qty):
        res = super(ProcurementOrder, self)._prepare_orderpoint_procurement(
            orderpoint, product_qty)
        if not orderpoint.group_id:
            group_id = self.env['procurement.group'].create({'name':'%s - %s' % (orderpoint.name, fields.Datetime.now() )})
            res['group_id'] = group_id.id
        return res
    
    @api.model
    def _product_virtual_get(self, order_point):
        res = super(ProcurementOrder, self)._product_virtual_get(order_point)

        other_res = order_point.product_id.with_context({'location':order_point.location_id.stock_location_ids.ids}).virtual_available
        
        if other_res < 0:
            other_res = 0
        
        return res + other_res
    
    
    @api.multi
    def get_mto_qty_to_order(self):
        self.ensure_one()
        uom_obj = self.env['product.uom']
        stock_location = self.warehouse_id.lot_stock_id.id
        proc_warehouse = self.with_context(location=stock_location)
        virtual_available = proc_warehouse.product_id.virtual_available
        qty_available = uom_obj._compute_qty(self.product_id.uom_id.id,
                                             virtual_available,
                                             self.product_uom.id)
        if qty_available > 0:
            if qty_available >= self.product_qty:
                return 0.0
            
        return self.product_qty
    
    @api.model
    def _run(self, procurement):
        ## prevent move within same location. Instead, change dest move to mts
        dest_move = procurement.move_dest_id
        if procurement.rule_id and procurement.rule_id.action == 'move' and \
            dest_move.id and procurement.rule_id.procure_method == 'make_to_stock' and \
            procurement.rule_id.location_id.id == procurement.rule_id.location_src_id.id:
                if dest_move.product_qty > procurement.product_qty:
                    new_move = dest_move.split(procurement.product_qty)
                    new_move.procure_method = 'make_to_stock'
                else:
                    dest_move.procure_method = 'make_to_stock'   
                return True
        return super(ProcurementOrder, self)._run(procurement)
