# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    grouped = fields.Boolean(
        string="Grouped",
        help="If checked, attribute will be used as a special type."
        " This attribute will be treated as select input type.",
    )
    group_suffix = fields.Char(
        "Group Suffix",
        help="Suffix for grouped attribute."
        " If filled, grouped attribute range will be"
        " displayed as 'value1 - value2 suffix'.",
    )

    def _get_grouped_range(self, ptal):
        """Returns the range of special type attributes."""

        self.ensure_one()
        value_list = [int(x) for x in ptal.value_ids.mapped("numeric_value")]
        if ptal.attribute_id.group_suffix:
            return "{} - {} {}".format(
                min(value_list), max(value_list), ptal.attribute_id.group_suffix
            )
        else:
            return ", ".join(str(x) for x in ptal.value_ids.mapped("name"))
