# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    is_published = fields.Boolean(
        string="Is Published",
        help="If checked, the attribute value will be published on the"
             " website.",
        default=False,
    )
