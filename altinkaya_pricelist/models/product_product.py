# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    sale_price = fields.Float(
        string="Sale Price", help="Sale price for e-commerce sales"
    )
