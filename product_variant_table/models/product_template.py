# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _build_product_variant_table(self):
        """This method groups variant attributes and returns a list of dictionaries.
        returns: attribute that sorted by value_ids count.
        """
        self.ensure_one()
        table_content = {
            "header": [],
            "rows": [],
            "has_special_attr": False,
            "special_attr": set(),
        }
        tmpl_id = self.sudo()

        for attr_line in tmpl_id.attribute_line_ids:
            if attr_line.attribute_id.visibility == "visible":
                table_content["header"].append(attr_line.attribute_id)

            if attr_line.attribute_id.special_type:
                table_content["has_special_attr"] = True

        for variant in tmpl_id.product_variant_ids.filtered(
            lambda p: p.is_published and p.sale_ok
        ):
            ptav = variant.product_template_variant_value_ids.filtered(
                lambda x: x.attribute_id.visibility == "visible"
            )

            if not ptav:  # skip if there is no visible attribute
                continue

            special_attr = ptav.filtered(lambda x: x.attribute_id.special_type)
            if special_attr:
                # pop special attribute from ptav
                table_content["special_attr"].add(special_attr)
                ptav -= special_attr

            table_content["rows"].append(ptav)

        if table_content["has_special_attr"]:
            # sort special rows by numeric value
            table_content["special_attr"] = sorted(
                table_content["special_attr"],
                key=lambda x: x.product_attribute_value_id.numeric_value,
            )

        # group rows if there is special attribute, so it won't be repeated
        table_content["rows"] = list(set(table_content["rows"]))
        # sort rows by attribute names
        table_content["rows"] = sorted(
            table_content["rows"],
            key=lambda v: v.mapped("product_attribute_value_id.name"),
        )

        return table_content
