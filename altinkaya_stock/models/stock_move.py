from odoo import models, fields, api
from odoo.tools import float_is_zero




#TODO @dogan:  not ported should check onur
class StockMove(models.Model):
    _inherit = 'stock.move'

    qty_available_sincan = fields.Float('Sincan Depo Mevcut', related='product_id.qty_available_sincan')
    qty_available_merkez = fields.Float('Merkez Depo Mevcut', related='product_id.qty_available_merkez')

    # def force_assign(self, moves):
    #     moves = self.env['stock.move'].search([('id', 'in', moves)])
    #     for move in moves:
    #         move.write({'state': 'assigned'})
    #     return True

    @api.multi
    def action_create_procurement(self):
        self.ensure_one()
        warehouses = self.env['stock.warehouse'].search([('selectable_on_procurement_wizard', '=', True)])
        if warehouses:
            qty_lines = [(0, 0, {
                'warehouse_id': wh.id,
                'warehouse_id_readonly': wh.id
            }) for wh in warehouses]
        else:
            qty_lines = []
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.procurement.move',
            'context': {'default_move_id': self.id, 'default_procurement_qty_ids': qty_lines},
            'target': 'new'
        }

    @api.multi
    def action_make_mts(self):
        self.ensure_one()
        return {
            'name': 'Pick from stock',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'make.mts.move',
            'context': {'default_move_id': self.id},
            'target': 'new'
        }

    @api.multi
    def action_view_origin_moves(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.name,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'stock.move',
            'domain': [('move_dest_ids', 'in', self.id)],
            'target': 'current'
        }
