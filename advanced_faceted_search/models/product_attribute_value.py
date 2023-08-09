# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class ProductAttributesValue(models.Model):
    _inherit = "product.attribute.value"

    def filter_available_values(self, category):
        possible_values = self.filtered(
            lambda v: v in category.available_attribute_value_ids
        )
        if len(possible_values) <= 1:
            return self.env["product.attribute.value"]
        else:
            return possible_values
