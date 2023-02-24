# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def get_all_variants(self):
        """Returns all available variants with ordered for the first attribute."""
        self.ensure_one()
        tmpl_id = self.sudo()
        variants = self.env["product.product"]
        for variant in tmpl_id.product_variant_ids:
            if any(
                [
                    c != "visible"
                    for c in variant.product_template_variant_value_ids.mapped(
                        "attribute_id.visibility"
                    )
                ]
            ):  # If any attribute is not visible, skip this variant
                continue

            if not variant.product_template_variant_value_ids:  # If no attributes, skip
                continue

            if variant.active and variant.website_published:
                variants |= variant

        # Sort variants by the attribute values.
        return variants.sorted(
            key=lambda v: v.mapped('product_template_variant_value_ids.product_attribute_value_id.name')
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
