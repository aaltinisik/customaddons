'''
Created on Jan 17, 2019

@author: cq
'''
from odoo import models,fields,api


#Aktarıldı


class ProductTemplate(models.Model):
    _inherit='product.template'
    
    
    
    has_production_bom = fields.Boolean('Has production BoM',compute='_compute_has_production_bom', store=True)
    
    @api.one
    @api.depends('bom_ids','bom_ids.type')
    def _compute_has_production_bom(self):
        self.has_production_bom = any(self.bom_ids.filtered(lambda b: b.type != 'phantom'))
        
        
class ProductCategory(models.Model):
    _inherit="product.category"
    
    
    x_guncelleme = fields.Char('Kategori Referansi',size=64,required=False)
    custom_products = fields.Boolean('Custom Products')

class ProductPriclelistItem(models.Model):
    _inherit = 'product.pricelist.item'
    
    
    x_guncelleme = fields.Char('Guncelleme Kodu',size=64)
