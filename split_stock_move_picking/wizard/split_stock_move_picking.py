from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SplitStockMovePicking(models.TransientModel):
    _name = 'split.stock.move.picking'
    _description = 'Splits stock.move in pickings'

    move_id = fields.Many2one('stock.move', 'Move', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', related='move_id.product_id', readonly=True)
    requested_qty = fields.Float('Talep Edilen', related="move_id.product_uom_qty", read_only=True)
    uom = fields.Many2one('uom.uom', string='UoM', related='move_id.product_uom', readonly=True)
    qty = fields.Float('Bölmek istediğiniz miktar')
    after_split_qty = fields.Float("Bölünmeden sonra miktar", readonly=True)

    @api.multi
    def action_split(self):
        if self.requested_qty - self.qty < 0.0:
            raise UserError(_(
                "Bölmek istediğiniz miktar talep edilenden daha fazla."))

        # copy as MTS
        self.move_id.copy({'product_uom_qty': self.qty,
                                 'created_production_id': 0,
                                 'created_purchase_line_id': 0,
                                 'procure_method': 'make_to_stock',
                                 'state': 'confirmed',
                                 # 'move_dest_ids': [
                                 #     (4, self.move_id.move_dest_ids.id)] if self.move_id.move_dest_ids else False
                                 })
        self.move_id.write({'product_uom_qty': self.move_id.product_uom_qty - self.qty})

        # # üretim emri varsa
        # if self.move_id.created_production_id:
        #     self.env['change.production.qty'].create({
        #         'mo_id': self.move_id.created_production_id.id,
        #         'product_qty': self.move_id.created_production_id.product_qty - self.qty
        #     }).change_prod_qty()
        #
        # # satınalma varsa
        # if self.move_id.created_purchase_line_id:
        #     self.move_id.created_purchase_line_id.write(
        #         {'product_qty': self.move_id.created_purchase_line_id.product_uom_qty - self.qty})

    @api.onchange('qty')
    def calc_qty_after_split(self):
        for move in self:
            move.after_split_qty = move.requested_qty - move.qty
