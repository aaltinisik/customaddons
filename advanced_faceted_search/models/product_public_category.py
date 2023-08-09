# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    available_attribute_value_ids = fields.Many2many(
        "product.attribute.value",
        compute="_compute_available_attribute_value_ids",
        string="Available Attribute Values",
        store=True,
    )

    def _compute_available_attribute_value_ids(self):
        """
        Compute available attribute values for each category.
        We are using this method because computing available attribute values
        for each category is a heavy process we don't want to do it
        every time.
        """
        for category in self.filtered(lambda c: c.is_published):
            attribute_value_ids = self.env["product.attribute.value"]
            products = self.env["product.template"].search(
                [
                    ("public_categ_ids", "in", category.ids),
                ]
            )
            if products:
                for product in products.filtered(lambda p: p.is_published):
                    for tmpl_line in list(product._get_possible_combinations()):
                        attribute_value_ids |= tmpl_line.mapped(
                            "product_attribute_value_id"
                        )
                category.available_attribute_value_ids = attribute_value_ids
            else:
                category.available_attribute_value_ids = False
