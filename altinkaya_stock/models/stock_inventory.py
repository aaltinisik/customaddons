# Copyright 2024 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, api


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    @api.model
    def _selection_filter(self):
        """
        Add negative_qty filter
        :return:
        """
        res = super(StockInventory, self)._selection_filter()
        res.append(("negative_qty", "Negative Quantities"))
        return res

    def _get_inventory_lines_values(self):
        """
        Filter out positive quantities if negative_qty filter is selected
        :return:
        """
        res = super(StockInventory, self)._get_inventory_lines_values()
        if self.filter == "negative_qty":
            res = [line for line in res if line["product_qty"] < 0]
        return res


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    @api.constrains("product_id")
    def _check_product_id(self):
        """
        Skip product type on negative_qty filter
        :return:
        """
        if self.inventory_id.filter == "negative_qty":
            return True
        else:
            return super(StockInventory, self)._check_product_id()
