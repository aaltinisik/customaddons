
from openerp import models, fields, api, _


class product_product(models.Model):
    _inherit = "product.product"

    qty_available_sincan = fields.Float('Sincan Depo Mevcut',compute='_compute_custom_available')
    qty_available_merkez = fields.Float('Merkez Depo Mevcut',compute='_compute_custom_available')
#    type_variant = fields.Selection([('product','Stockable Product'),('consu','Consumable'),('service','Service')], string="Product Type", default=False,store=True)
#    type = fields.Selection([('product','Stockable Product'),('consu','Consumable'),('service','Service')],compute='_compute_type')
    
    
#    @api.multi
#    def _compute_type(self):
#        for product in self:
#            product.type = product.type_variant or product.product_tmpl_id.type
            
    
    @api.multi
    def _compute_custom_available(self):
        for product in self:
            product.qty_available_sincan = product.with_context({'location':28}).qty_available
            product.qty_available_merkez = product.with_context({'location':10}).qty_available
    
