# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    special_type = fields.Boolean(
        string="Special Type",
        help="If checked, attribute will be used as a special type."
        " This attribute will be treated as select input type.",
    )

    def _get_special_type_range(self, ptal):
        """Returns the range of special type attributes.
        """

        self.ensure_one()
        value_list = [int(x) for x in ptal.value_ids.mapped("numeric_value")]
        return "{} mm - {} mm".format(min(value_list), max(value_list))
