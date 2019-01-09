'''
Created on Nov 27, 2017

@author: dogan
'''


from openerp import models, fields, api
from openerp.osv import fields as osv_fields
from openerp.tools.translate import _
from openerp import exceptions
from openerp.tools import mute_logger

from openerp.osv.orm import browse_record

import openerp

import psycopg2

class ProductMoveWizard(models.TransientModel):
    _name = 'product.move.wizard'
    
    product_id = fields.Many2one('product.product','Product', default=lambda self: self._default_product())
    product_tmpl_id = fields.Many2one('product.template','New Product Name', required=True)
    value_ids = fields.Many2many('product.attribute.value',string='Attribute Value IDs')
    
    @api.model
    def _default_product(self):
        if self._context.get('active_id', False):
            return self.env['product.product'].search([('id','=',self._context['active_id'])])[0]
        else:
            raise exceptions.Warning(_('Wrong context propagation'))
        
    @api.onchange('product_id')
    def onchange_product_id(self):
        self.product_tmpl_id = self.product_id.product_tmpl_id
        
    
    @api.onchange('product_tmpl_id','value_ids')
    def onchange_value_ids(self):
        existing_attribute_ids = self.value_ids.mapped('attribute_id.id')
        product_tmpl_attr_ids = self.product_tmpl_id.attribute_line_ids.mapped('attribute_id.id')
        existing_product_attribute_value_ids = self.product_id.attribute_value_ids.filtered(lambda self: self.attribute_id.id in product_tmpl_attr_ids)
        self.value_ids = [(6, False, existing_product_attribute_value_ids.ids)]
        return {'domain':{'value_ids':[('id','in', self.product_tmpl_id.attribute_line_ids.mapped('value_ids.id')),
                                  ('attribute_id','not in',existing_attribute_ids)]}
                }
            
       
    
    
    @api.multi
    def action_move(self):
        self.ensure_one()
        self.product_id.write({'product_tmpl_id':self.product_tmpl_id.id,
                               'attribute_value_ids':[(6,False, self.value_ids.ids)]
                               })
       
        
        
        
        
    
    
    


    