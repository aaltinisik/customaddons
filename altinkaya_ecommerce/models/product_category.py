# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"
    _order = "sequence, complete_name"

    sequence = fields.Integer(
        string="Sequence",
        default=100,
        help="Gives the sequence order when displaying a list of product categories.",
    )

    is_published = fields.Boolean(
        string="Published",
        default=False,
        help="If unchecked, it will allow you to hide the category without removing it.",
    )
