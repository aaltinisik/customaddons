# -*- coding: utf-8 -*-
'''
Created on Jul 18, 2016

@author: Codequarters_ugur
'''

from openerp import models, fields, api


class product_product(models.Model):
    _inherit = 'product.product'

    route_ids= fields.Many2many('stock.location.route', string='Routes', domain="[('product_selectable', '=', True)]",
                                    compute='_compute_variant_routes')
    
    variant_route_ids= fields.Many2many('stock.location.route','stock_route_product_variant', 'product_id', 'route_id',
                                        string='Variant Routes')
    
    variant_route_num = fields.Integer('Variant Routes',compute='_compute_variant_routes')
    
    @api.one
    @api.depends('variant_route_ids')
    def _compute_variant_routes(self):
        self.variant_route_num = len(self.variant_route_ids)
        if self.variant_route_num > 0:
            self.route_ids = self.variant_route_ids
        else:
            self.route_ids = self.product_tmpl_id.route_ids
    
    
        