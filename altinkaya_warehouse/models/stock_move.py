
from openerp import models, fields


class stock_move(models.Model):
    _inherit = "stock.move"

    qty_available_sincan = fields.Float('Sincan Depo Mevcut',related='product_id.qty_available_sincan')
    qty_available_merkez = fields.Float('Merkez Depo Mevcut',related='product_id.qty_available_merkez')
