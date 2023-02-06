# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    base = fields.Selection(
        selection_add=[("sale_price", "Website Sale Price")],
        ondelete={"sale_price": "set default"},
    )
