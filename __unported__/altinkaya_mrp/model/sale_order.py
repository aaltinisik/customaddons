# -*- coding: utf-8 -*-

from openerp import models, fields, api


class sale_order(models.Model):
    _inherit = 'sale.order'
    
    
    production_ids = fields.Many2many('mrp.production',string='Manufacturing Orders', compute='_compute_productions')
    
    @api.multi
    def _compute_productions(self):
        for so in self:
            so.production_ids = self.env['mrp.production'].search([('sale_id','=', so.id)])
        