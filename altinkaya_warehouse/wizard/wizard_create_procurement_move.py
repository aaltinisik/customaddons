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
    
    move_qty = fields.Float('Demand Quantity', related='move_id.product_uom_qty', readonly=True)
    qty_to_sincan = fields.Float('Quantity to Sincan Depo')
    qty_to_ivedik = fields.Float('Quantity to Ivedik Depo')
    
    uom = fields.Many2one('product.uom', string='UoM', related='move_id.product_uom', readonly=True)
    
    @api.onchange('move_id')
    def onchange_move_id(self):
        self.qty = self.move_id.remaining_qty
        
    
    @api.multi
    def action_create(self):
        self.ensure_one()
        self.move_id.action_cancel()
        self.move_id.procure_method = 'make_to_order'
        self.move_id.action_confirm()
        
        procurement_ids = self.move_id.move_orig_ids.mapped('procurement_id')
        
        if self.qty_to_sincan > 0.0:
            wh = self.env['stock.warehouse'].browse([3])
            procure_id = self.env['procurement.order'].create({
                'name':'INT: %s' % self.env.user.name,
                'date_planned': self.move_id.date_expected,
                'product_id': self.product_id.id,
                'product_qty': self.qty_to_sincan,
                'product_uom': self.uom.id,
                'warehouse_id': wh.id,
                'location_id': wh.lot_stock_id.id,
                'company_id': wh.company_id.id,
            })
            procure_id.signal_workflow( 'button_confirm')
            procurement_ids |= procure_id
            
        if self.qty_to_ivedik > 0.0:
            wh = self.env['stock.warehouse'].browse([2])
            procure_id = self.env['procurement.order'].create({
                'name':'INT: %s' % self.env.user.name,
                'date_planned': self.move_id.date_expected,
                'product_id': self.product_id.id,
                'product_qty': self.qty_to_ivedik,
                'product_uom': self.uom.id,
                'warehouse_id': wh.id,
                'location_id': wh.lot_stock_id.id,
                'company_id': wh.company_id.id,
            })
            procure_id.signal_workflow( 'button_confirm')
            procurement_ids |= procure_id
        
        data_obj = self.env['ir.model.data']            
        
        
        id2 = data_obj.xmlid_to_res_id('procurement.procurement_tree_view')# data_obj._get_id('procurement', 'procurement_tree_view')
        id3 = data_obj.xmlid_to_res_id('procurement.procurement_form_view')

        action = {
            'name': 'Procurements',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'procurement.order',
            'type': 'ir.actions.act_window'
        }
        
        if len(procurement_ids) > 1:
            action.update({'domain' : [('id','in',procurement_ids.ids)] })
        elif len(procurement_ids) == 1:
            
            action.update({'res_id' : procurement_ids[0].id ,
                           'views': [(id3,'form'),(id2,'tree')]})
        else:
            return {}
        
        return action
        
        
        
        