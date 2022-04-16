# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_compare, float_is_zero


class UpdateUnreservedQuants(models.TransientModel):
    """
    See:
    https://gist.github.com/amoyaux/279aee13eaddacbddb435dafbc0a6295
    https://gist.github.com/ryanc-me/632fd59639a8a68e041c876abe87168f
    """

    _name = 'update.unreserved.quants'
    _description = 'Update Unreserved Quants'

    @api.multi
    def action_update_unreserved_quants(self):
        """
        Fix unreserved quants.
        """
        StockQuant = self.env['stock.quant']
        StockMoveLine = self.env['stock.move.line']
        decimal_places = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        quant_query = """
            SELECT *
            FROM stock_quant
        """
        self.env.cr.execute(quant_query)
        quants = self.env.cr.dictfetchall()
        for quant in quants:
            ml_query = """
                SELECT product_qty from stock_move_line
                 WHERE product_id = %s
                    AND location_id = %s
                    AND lot_id = %s
                    AND package_id = %s
                    AND owner_id = %s
                    AND product_qty > 0
            """
            self.env.cr.execute(ml_query)
            move_lines = self.env.cr.dictfetchall()
            if move_lines:
                ml_qty = sum(ml['product_qty'] for ml in move_lines)
                ml_qty
                # move_lines = StockMoveLine.search(
                #     [
                #         ("product_id", "=", quant.product_id.id),
                #         ("location_id", "=", quant.location_id.id),
                #         ("lot_id", "=", quant.lot_id.id),
                #         ("package_id", "=", quant.package_id.id),
                #         ("owner_id", "=", quant.owner_id.id),
                #         ("product_qty", "!=", 0),
                #     ]
                # )
                # if quant.location_id.should_bypass_reservation():
                #     # If a quant is in a location that should bypass the reservation, its `reserved_quantity` field
                #     # should be 0.
                #     if not float_is_zero(quant.reserved_quantity, precision_digits=decimal_places):
                #         quant.write({"reserved_quantity": 0})
                # else:
                #     raw_reserved_qty = sum(move_lines.mapped('product_qty'))
                #     if float_compare(quant.reserved_quantity, raw_reserved_qty, precision_digits=decimal_places) != 0:
                #         quant.write({
                #             'reserved_quantity': raw_reserved_qty
                #         })