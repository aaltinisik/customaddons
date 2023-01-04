# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"
    _order = "sequence, complete_name"

    is_published = fields.Boolean(
        string="Published",
        help="If unchecked, it will allow you to hide the category without removing it.",
        default=True,
    )

    sequence = fields.Integer(
        string="Sequence",
        help="Gives the sequence order when displaying a list of product categories.",
        default=100,
    )

