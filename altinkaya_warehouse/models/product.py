
from openerp import models, fields, api, _


class product_template(models.Model):
    _inherit = "product.product"

    qty_available_sincan = fields.Float('Sincan Depo Mevcut',compute='_compute_custom_available')
    qty_available_merkez = fields.Float('Merkez Depo Mevcut',compute='_compute_custom_available')
    
    
    @api.multi
    def _compute_custom_available(self):
        for product in self:
            product.qty_available_sincan = product.with_context({'location':28}).qty_available
            product.qty_available_merkez = product.with_context({'location':10}).qty_available
    
