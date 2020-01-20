'''
Created on Jan 17, 2019

@author: cq
'''
from odoo import models,fields,api
from odoo.addons import decimal_precision as dp

#Aktarıldı
class product_attribute_line(models.Model):
    _inherit = 'product.template.attribute.line'
    attr_base_price =fields.Float(
             u"Base Price",
             digits=dp.get_precision('Product Price'),
             help=u"Base price used to compute product price based on attribute value.")
    attr_val_price_coef= fields.Float(
             u"Value Price Multiplier",
             digits=dp.get_precision('Product Price'),
             help=u"Attribute value coefficient used to compute product price based on attribute value.")
    use_in_pricing = fields.Boolean('Use in pricing')
    

class ProductTemplate(models.Model):
    _inherit='product.template'
    
    
    
    has_production_bom = fields.Boolean('Has production BoM',compute='_compute_has_production_bom', store=True)
    
    @api.one
    @api.depends('bom_ids','bom_ids.type')
    def _compute_has_production_bom(self):
        self.has_production_bom = any(self.bom_ids.filtered(lambda b: b.type != 'phantom'))
        


