# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"
    _order = "sequence, name"

    sequence = fields.Integer(
        string="Sequence",
        default=100,
        help="Gives the sequence order when displaying a list of product categories.",
    )
