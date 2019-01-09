# -*- encoding: utf-8 -*-
#
#Created on Oct 12, 2018
#
#@author: dogan
#

from openerp import models, fields, api
from openerp.exceptions import ValidationError


class create_despatch(models.TransientModel):
    _name = 'create.picking.despatch'
    
    
    @api.model
    def _default_picking_ids(self):
        if self._context.get('active_model',False) != 'stock.picking':
            raise ValidationError('Wrong context propagation')
        
        selected_pickings = self.env['stock.picking'].search([('id','in',self._context.get('active_ids',[]))])
        already_dispatched = selected_pickings.filtered(lambda p: p.despatch_id.id)
        if len(already_dispatched) > 0:
            raise ValidationError('Already despatched pickings selected!\n%s' % '\n'.join(already_dispatched.mapped('name')))
        
        return selected_pickings
        
    carrier_id = fields.Many2one('delivery.carrier','Carrier')
    picking_ids = fields.Many2many('stock.picking',string='Pickings to dispatch', default=lambda self: self._default_picking_ids())
    
    
    @api.multi
    def action_create(self):
        DispatchObj = self.env['stock.picking.despatch']
        
        despatch_id = DispatchObj.create({'carrier_id':self.carrier_id.id,
                            'picking_ids':[(6,False, self.picking_ids.ids)]})
        
        self.picking_ids.write({'despatch_id':despatch_id.id})
        
        return {
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking.despatch',
            'res_id' : despatch_id.id,
            'type': 'ir.actions.act_window',
         }