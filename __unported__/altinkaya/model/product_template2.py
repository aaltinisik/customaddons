# -*- encoding: utf-8 -*-

from openerp import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.template'
    
    has_production_bom = fields.Boolean('Has production BoM',compute='_compute_has_production_bom', store=True)
    
    @api.one
    @api.depends('bom_ids','bom_ids.type')
    def _compute_has_production_bom(self):
        self.has_production_bom = any(self.bom_ids.filtered(lambda b: b.type != 'phantom'))
        