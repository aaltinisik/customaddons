# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    excluded_product_ids = fields.Many2many(
        "product.template",
        string="Excluded Products",
        help="Products that will not be shown in the website.",
    )

    excluded_product_category_ids = fields.Many2many(
        "product.public.category",
        string="Excluded Product Categories",
        help="Product categories that will not be shown in the website.",
    )
