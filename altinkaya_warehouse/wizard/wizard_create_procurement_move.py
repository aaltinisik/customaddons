# -*- encoding: utf-8 -*-
#
#Created on Oct 12, 2018
#
#@author: dogan
#

from openerp import models, fields, api
from openerp.exceptions import ValidationError
from openerp.tools import float_compare


class create_despatch(models.TransientModel):
    _name = 'create.procurement.move'
        
    move_id = fields.Many2one('stock.move','Move', readonly=True)
    product_id = fields.Many2one('product.product',string='Product', related='move_id.product_id', readonly=True)
    qty = fields.Float('Requested Quantity')
    uom = fields.Many2one('product.uom', string='UoM', related='move_id.product_uom', readonly=True)
    
    @api.onchange('move_id')
    def onchange_move_id(self):
        self.qty = self.move_id.remaining_qty
        
    
    @api.multi
    def action_create(self):
        self.ensure_one()
        
        if float_compare(self.qty, 0.0, precision_rounding=self.uom.rounding) <= 0:
            return
        
        qty_to_split = 0.0
        qty_to_add = 0.0
        
        comparison = float_compare(self.qty, self.move_id.remaining_qty, precision_rounding=self.uom.rounding)
        
        if comparison <= 0.0:
            qty_to_split = self.qty
            qty_to_add = 0.0
        
        elif comparison > 0.0:
            qty_to_split = self.move_id.remaining_qty
            qty_to_add = self.qty - self.move_id.remaining_qty 
        
        
        if qty_to_split == self.qty:
            self.move_id.action_cancel()
            self.move_id.procure_method = 'make_to_order'
            self.move_id.action_confirm()
            
        elif qty_to_split > 0.0:
            
            defaults = {
                'product_uom_qty': qty_to_split,
                'product_uos_qty': qty_to_split,
                'procure_method': 'make_to_order',
                'restrict_lot_id': self.move_id.restrict_lot_id.id,
                'split_from': self.move_id.id,
                'procurement_id': self.move_id.procurement_id.id,
                'move_dest_id': self.move_id.move_dest_id.id,
                'origin_returned_move_id': self.move_id.origin_returned_move_id.id,
                'restrict_partner_id': self.move_id.restrict_partner_id.id,
            }
    
            
            new_move = self.move_id.copy(defaults)
            
            self.move_id.with_context({'do_not_propagate':True}).write({
                'product_uom_qty': self.move_id.product_uom_qty - qty_to_split,
                'product_uos_qty': self.move_id.product_uos_qty - qty_to_split
            })
    
            
            new_move.action_confirm()
            
        if qty_to_add > 0.0:
            wh = self.move_id.warehouse_id
            procure_id = self.env['procurement.order'].create({
                'name':'INT: %s' % self.env.user.name,
                'date_planned': self.move_id.date_expected,
                'product_id': self.product_id.id,
                'product_qty': qty_to_add,
                'product_uom': self.uom.id,
                'warehouse_id': wh.id,
                'location_id': wh.lot_stock_id.id,
                'company_id': wh.company_id.id,
            })
            procure_id.signal_workflow( 'button_confirm')
            
        
        return {}
        
        