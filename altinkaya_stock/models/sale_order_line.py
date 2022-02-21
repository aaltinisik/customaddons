from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_available_sincan = fields.Float('Sincan Depo Mevcut',related='product_id.qty_available_sincan')
    qty_available_merkez = fields.Float('Merkez Depo Mevcut',related='product_id.qty_available_merkez')