# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def get_all_variants(self):
        """Returns all available variants with ordered for the first attribute."""
        self.ensure_one()
        variants = self.product_variant_ids.filtered(
            lambda p: p.active and p.website_published
        )
        return variants.sorted(
            key=lambda v: v.product_template_attribute_value_ids[0].attribute_id.name
        )

    # @api.model
    # def _build_variant_select_table(self):
    #     """Build a table of product variants."""
    #     self.ensure_one()
    #     active_variant_ids = self.product_variant_ids.filtered(
    #         lambda p: p.active and p.website_published
    #     )
    #     active_attr_ids = active_variant_ids.mapped("attribute_line_ids.attribute_id")
    #     variant_table = {
    #         "header": active_attr_ids,
    #         "rows": [],
    #     }
    #
    #     for product_variant in active_variant_ids:
    #         row = {
    #             "product_variant_id": product_variant,
    #             "product_variant_values": [],
    #         }
    #         for attr in active_attr_ids:
    #             row["product_variant_values"].append(
    #                 product_variant.product_template_attribute_value_ids.filtered(
    #                     lambda v: v.attribute_id == attr
    #                 ).product_attribute_value_id
    #             )
    #         variant_table["rows"].append(row)
    #     return variant_table
