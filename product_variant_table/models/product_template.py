# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, models
from collections import OrderedDict


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
            key=lambda v: v.mapped(
                "product_template_variant_value_ids.product_attribute_value_id.name"
            )
        )

    def new_method_yigit(self):
        """This method groups variant attributes and returns a list of dictionaries.
        returns: attribute that sorted by value_ids count.
        """
        self.ensure_one()
        res = {}
        tmpl_id = self.sudo()
        for variant in tmpl_id.product_variant_ids:
            ptav = variant.product_template_variant_value_ids
            for ptav_id in ptav.filtered(
                lambda x: x.attribute_id.visibility == "visible"
            ):

                if ptav_id.attribute_id not in res:
                    res[ptav_id.attribute_id] = {
                        "special_type": ptav_id.attribute_id.special_type,
                        "value_ids": self.env["product.attribute.value"],
                    }
                res[ptav_id.attribute_id][
                    "value_ids"
                ] |= ptav_id.product_attribute_value_id

        # sort by value_ids count return as dict
        return OrderedDict(sorted(res.items(), key=lambda i: len(i[1])))
