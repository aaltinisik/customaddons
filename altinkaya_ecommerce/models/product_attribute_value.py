# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    numeric_value = fields.Float(
        string="Numeric Value",
        digits=(16, 6),
        help="Numeric value of the attribute value. We use this field to sort the"
             " attribute values currently",
    )
