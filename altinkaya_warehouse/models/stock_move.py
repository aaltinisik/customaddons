
from openerp import models, fields, api


class stock_move(models.Model):
    _inherit = "stock.move"

    qty_available_sincan = fields.Float('Sincan Depo Mevcut',related='product_id.qty_available_sincan')
    qty_available_merkez = fields.Float('Merkez Depo Mevcut',related='product_id.qty_available_merkez')
    
    
    @api.model
    def _prepare_procurement_from_move(self, move):
        res = super(stock_move, self)._prepare_procurement_from_move( move)
        if res and 'sale_line_id' not in res:
            sale_line_id = move.procurement_id.sale_line_id.id or move.raw_material_production_id.move_prod_id.procurement_id.sale_line_id.id
            res.update({'sale_line_id':sale_line_id})
                
        return res
    
    @api.multi
    def action_create_procurement(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.procurement.move',
            'context' : {'default_move_id':self.id},
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
            'domain' : [('move_dest_id','=', self.id)],
            'target': 'current'
         }

    @api.model
    def _create_procurements(self, moves):
        res = super(stock_move, self)._create_procurements(moves)
        moves_to_remove = []
        for move in moves:
            if move.procure_method == 'make_to_stock':
                moves_to_remove.append(move)

        for tm in moves_to_remove:
            moves.remove(tm)

            
        return res