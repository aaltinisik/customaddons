# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    # we use this field instead of the default one to avoid the problem of
    # the default one doesn't compute the default product_id
    variant_seller_ids_2 = fields.One2many(
        "product.supplierinfo",
        inverse_name="product_id",
    )
