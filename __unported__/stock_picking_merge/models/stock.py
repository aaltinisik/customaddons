# -*- coding: utf-8 -*-

from openerp import api, fields, models, _


class stock_picking(models.Model):
    _inherit = "stock.picking"

    @api.one
    def calculate_merged_pickings(self):
        self.total_merged_pickings = len(self.merge_picking_ids.ids)

    total_merged_pickings = fields.Integer(string="Pickings", compute=calculate_merged_pickings)
    merge_picking_ids = fields.Many2many('stock.picking', 'picking_merged_rel', 'picking_id', 'merge_id', string="Merged Pickings")

    @api.multi
    def show_merged_pickings(self):
        tree_view = self.env.ref('stock.vpicktree')
        form_view = self.env.ref('stock.view_picking_form')
        return {
            'name': 'Merged Pickings',
            'domain': [('id','in',self.merge_picking_ids.ids)],
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'views': [(tree_view.id, 'tree'), (form_view.id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'current',
            'nodestroy': True
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
