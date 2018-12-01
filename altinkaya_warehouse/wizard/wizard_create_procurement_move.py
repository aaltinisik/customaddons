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
    procure_move  = fields.Boolean('Harekete Tedarik Oluştur',default=True)
    qty_to_sincan = fields.Float('Quantity to Sincan Depo')
    qty_to_merkez = fields.Float('Quantity to Merkez Depo')
    qty_available_merkez = fields.Float('Merkez Depo Mevcut', related='product_id.qty_available_merkez')
    qty_available_sincan = fields.Float('Sincan Depo Mevcut', related='product_id.qty_available_sincan')
    qty_incoming_merkez = fields.Float('Merkez Depo Gelen', related='product_id.qty_incoming_merkez')
    qty_incoming_sincan = fields.Float('Sincan Depo Gelen', related='product_id.qty_incoming_sincan')
    qty_outgoing_merkez = fields.Float('Merkez Depo Giden', related='product_id.qty_outgoing_merkez')
    qty_outgoing_sincan = fields.Float('Sincan Depo Giden', related='product_id.qty_outgoing_sincan')
    qty_virtual_merkez = fields.Float('Merkez Depo Tahmini', related='product_id.qty_virtual_merkez')
    qty_virtual_sincan = fields.Float('Sincan Depo Tahmini', related='product_id.qty_virtual_sincan')
    uom = fields.Many2one('product.uom', string='UoM', related='move_id.product_uom', readonly=True)
    
    production_ids = fields.Many2many('mrp.production',string='Manufacturing Orders', compute='_compute_productions')
    transfers_to_customer_ids = fields.Many2many('stock.move',string='Transfers to Customers', compute='_compute_customer_transfers')
    
    @api.multi
    @api.depends('product_id')
    def _compute_productions(self):
        for wizard in self:
            wizard.production_ids = self.env['mrp.production'].search([('product_id','=',wizard.product_id.id),('state','not in', ['done','cancel'])])

    @api.multi
    @api.depends('product_id')
    def _compute_customer_transfers(self):
        for wizard in self:
            wizard.transfers_to_customer_ids = self.env['stock.move'].search([('product_id','=',wizard.product_id.id),('state','not in', ['draft','done','cancel'])])

    @api.onchange('move_id')
    def onchange_move_id(self):
        self.qty = self.move_id.remaining_qty
        
    
    @api.multi
    def action_create(self):
        self.ensure_one()
        if self.procure_move:
            self.move_id.action_cancel()
            self.move_id.procure_method = 'make_to_order'
            self.move_id.action_confirm()
            procurement_ids = self.move_id.move_orig_ids.mapped('procurement_id')
        
        if self.qty_to_sincan > 0.0:
            wh = self.env['stock.warehouse'].browse([28])
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
            
        if self.qty_to_merkez > 0.0:
            wh = self.env['stock.warehouse'].browse([10])
            procure_id = self.env['procurement.order'].create({
                'name':'INT: %s' % self.env.user.name,
                'date_planned': self.move_id.date_expected,
                'product_id': self.product_id.id,
                'product_qty': self.qty_to_merkez,
                'product_uom': self.uom.id,
                'warehouse_id': wh.id,
                'location_id': wh.lot_stock_id.id,
                'company_id': wh.company_id.id,
            })
            procure_id.signal_workflow( 'button_confirm')
            procurement_ids |= procure_id
        
        data_obj = self.env['ir.model.data']            
        
        
        id2 = data_obj.xmlid_to_res_id('procurement.procurement_tree_view')
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
        
        
        
        
