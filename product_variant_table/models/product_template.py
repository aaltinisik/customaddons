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
            "rows": set(),
            "has_grouped_attr": False,
            "grouped_attr": {},
        }
        tmpl_id = self.sudo()

        for attr_line in tmpl_id.attribute_line_ids:
            if attr_line.attribute_id.visibility == "visible":
                table_content["header"].append(attr_line.attribute_id)

            if attr_line.attribute_id.grouped:
                table_content["has_grouped_attr"] = True
                table_content["grouped_attr"].update({attr_line.attribute_id: set()})

        sale_variants = tmpl_id.product_variant_ids.filtered(
            lambda p: p.is_published and p.sale_ok
        )
        variant_count = self._get_common_attr_count(sale_variants)

        for variant in sale_variants:
            ptav = variant.product_template_attribute_value_ids.filtered(
                lambda x: x.attribute_id.visibility == "visible"
            )

            if not ptav:  # skip if there is no visible attribute
                continue

            if len(ptav) != variant_count:
                # skip if there is no common attribute
                continue

            for grouped_attr in ptav.filtered(lambda x: x.attribute_id.grouped):
                # pop grouped attribute from ptav
                table_content["grouped_attr"][grouped_attr.attribute_id].add(
                    grouped_attr
                )
                ptav -= grouped_attr

            table_content["rows"].add(ptav)

        if table_content["has_grouped_attr"]:
            # sort grouped rows by numeric value
            for attr_id, attr_vals in table_content["grouped_attr"].items():
                table_content["grouped_attr"][attr_id] = sorted(
                    attr_vals,
                    key=lambda x: x.product_attribute_value_id.numeric_value,
                )

        # sort rows by attribute names
        table_content["rows"] = sorted(
            list(table_content["rows"]),
            key=lambda v: v.mapped("product_attribute_value_id.name"),
        )
        # sort table header to match with rows
        table_content["header"] = sorted(
            table_content["header"],
            key=lambda x: x.grouped,
        )

        return table_content

    def _get_common_attr_count(self, variants):
        """
        This method returns the number of common attributes.
        """
        attr_counts = []
        for variant in variants:
            ptav = variant.product_template_attribute_value_ids.filtered(
                lambda x: x.attribute_id.visibility == "visible"
            )
            attr_counts.append(len(ptav))

        return max(attr_counts)
