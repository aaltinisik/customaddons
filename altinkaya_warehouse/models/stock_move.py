
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
