# -*- coding: utf-8 -*-

from openerp import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    @api.onchange('routing_id')
    def onchange_routing_id(self):
        if self.routing_id.location_id:
            self.location_src_id = self.routing_id.location_id
            self.location_dest_id = self.routing_id.location_id
            
            
    @api.model
    def _make_consume_line_from_data(self, production, product, uom_id, qty,
                                     uos_id, uos_qty):
        move_id = super(MrpProduction, self)._make_consume_line_from_data(
            production, product, uom_id, qty, uos_id, uos_qty)
        self.env['stock.move'].browse([move_id]).priority = production.priority
        return move_id
    
    
    @api.multi
    def action_confirm(self):
        res = super(MrpProduction, self).action_confirm()
        self.action_assign()
        return res