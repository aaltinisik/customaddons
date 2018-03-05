# -*- encoding: utf-8 -*-
#
#Created on Mar 5, 2018
#
#@author: dogan
#
from openerp import models, fields, api


class MrpBoM(models.Model):
    _inherit= 'mrp.bom'
    
    @api.model
    def _prepare_consume_line(self, bom_line, quantity, factor=1):
        product_qty = quantity
        
        if bom_line.factor_attribute_id:
            attribute_value_ids = bom_line.bom_id.product_id.attribute_value_ids
            attribute_value_id = attribute_value_ids.filtered(lambda v: v.attribute_id.id == bom_line.factor_attribute_id.id)
            if attribute_value_id:
                product_qty = quantity + (attribute_value_id.numeric_value * bom_line.attribute_factor)
            
                
        
        res = super(MrpBoM, self)._prepare_consume_line(bom_line, product_qty, factor)
        return res
    
        
        
    
class MrpBoMLine(models.Model):
    _inherit = 'mrp.bom.line'
    
    factor_attribute_id = fields.Many2one('product.attribute',string='Factor Attribute',
                                          help='End product attribute to use for raw material calculation')
    attribute_factor = fields.Float(string='Factor',help='Factor to multiply by the numeric value of attribute')
    
    