# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _cart_update_order_line(self, product_id, quantity, order_line, **kwargs):
        order_line = super(SaleOrder, self)._cart_update_order_line(
            product_id, quantity, order_line, **kwargs
        )
        if order_line and order_line.set_product:
            # since we have nothing to do with the return value of this method,
            # we can just return a dummy sale order line
            dummy_sol = order_line.explode_set_contents()
            return dummy_sol
        return order_line
