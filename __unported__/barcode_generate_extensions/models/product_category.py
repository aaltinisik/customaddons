

from odoo import models,fields







class ProductCategory(models.Model):
    _inherit='product.category'
    
    
    
    barcode_rule_id = fields.Many2one('barcode.rule','Barcode Rule')