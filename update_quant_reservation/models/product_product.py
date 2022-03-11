from odoo import models, fields, api, _
from odoo.exceptions import Warning

class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_fix_reservation(self):
        moves = self.env['stock.move'].search([('product_id', '=', self.id),
                                               ('state', 'not in', ['done', 'cancel'])])
        for move in moves:
            move._do_unreserve()

        for quant in self.stock_quant_ids:
            quant.write({'reserved_quantity': 0.0})

        # quants = self.env['stock.quant'].search([('product_id', '=', self.id)])
        # messages = []
        # for quant in quants:
        #     move_lines = self.env["stock.move.line"].search(
        #         [
        #             ("product_id", "=", quant.product_id.id),
        #             ("location_id", "=", quant.location_id.id),
        #             ("lot_id", "=", quant.lot_id.id),
        #             ("package_id", "=", quant.package_id.id),
        #             ("owner_id", "=", quant.owner_id.id),
        #             ("product_qty", "!=", 0),
        #         ]
        #     )
        #
        #     if quant.location_id.should_bypass_reservation():
        #         # If a quant is in a location that should bypass the reservation, its `reserved_quantity` field
        #         # should be 0.
        #         if quant.reserved_quantity != 0:
        #             quant.write({"reserved_quantity": 0})
        #             adjust_msg = "Adjusted bypass-reservation location:"
        #             adjust_msg += "\n - Location (%s): %s" % (str(quant.location_id.id), quant.location_id.display_name)
        #             adjust_msg += "\n - Product (%s): %s" % (str(quant.product_id.id), quant.product_id.display_name)
        #             adjust_msg += "\n - Quantity: (%s)" % str(quant.reserved_quantity)
        #             messages.append(adjust_msg)
        #     else:
        #         # we need to round qty after summing, but we can't import float_round
        #         # instead, use the _compute_qty() function. it's designed to convert from
        #         # one UoM to another, and will round to the UoM's precision. we can
        #         # provide the product UoM twice to 'convert' to/from the same UoM,
        #         # resulting in the same qty, but rounded!
        #
        #         raw_reserved_qty = sum(move_lines.mapped('product_qty'))
        #         for move in move_lines:
        #             move_reserved_qty = move.product_id.uom_id._compute_quantity(raw_reserved_qty,
        #                                                                                move.product_id.uom_id)
        #             quant_reserved_qty = move.product_id.uom_id._compute_quantity(quant.reserved_quantity,
        #                                                                                 move.product_id.uom_id)
        #
        #             if quant_reserved_qty != move_reserved_qty:
        #                 quant.write({
        #                     'reserved_quantity': move_reserved_qty
        #                 })
        #                 adjust_msg = "Adjusted reservation discrepancy:"
        #                 adjust_msg += "\n - Location (%s): %s" % (str(quant.location_id.id), quant.location_id.display_name)
        #                 adjust_msg += "\n - Product (%s): %s" % (str(quant.product_id.id), quant.product_id.display_name)
        #                 adjust_msg += "\n - Quantity: (quant=%s) (move=%s)" % (
        #                 str(quant_reserved_qty), str(move_reserved_qty))
        #                 adjust_msg += "\n - Move IDs: %s" % (', '.join([str(l.id) for l in move]))
        #                 adjust_msg += "\n - Details: \n    * %s" % ('\n    * '.join(
        #                     [('%s: %s (origin: %s)' % (str(l.id), l.product_qty, l.origin)) for l in move]))
        #                 messages.append(adjust_msg)
        #
        # if messages:
        #     raise Warning(_('\n\n'.join(messages)))
