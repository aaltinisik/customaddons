# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class stock_move(models.Model):
    _inherit = 'stock.move'
    
    @api.multi
    def action_print_product_label(self):
        
        self.ensure_one()
        res = self.product_id.action_print_label()
        res['context'].update({'active_ids':[self.product_id.id]})
        return res
        
        
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
