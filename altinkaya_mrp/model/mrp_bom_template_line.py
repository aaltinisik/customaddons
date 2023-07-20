# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api

class MrpBomTemplateLine(models.Model):
    _name = "mrp.bom.template.line"
    _description = "Mrp Bom Template Lines"
    _order = "sequence, id"

    name = fields.Char(
        string="Name",
        related="product_tmpl_id.name",
        readonly=True,
    )

    sequence = fields.Integer(
        string="Sequence",
        default=100,
    )

    bom_id = fields.Many2one(
        "mrp.bom",
        string="Bom Template",
    )

    bom_product_id = fields.Many2one(
        "product.template",
        string="Bom Product",
        related="bom_id.product_tmpl_id",
    )

    product_tmpl_id = fields.Many2one(
        "product.template",
        string="Product Template",
        required=True,
    )

    product_qty = fields.Float(
        string="Quantity",
        default=1.0,
        required=True,
    )

    product_uom_id = fields.Many2one(
        "uom.uom",
        string="Unit of Measure",
        required=True,
        default=lambda self: self.env.ref("uom.product_uom_unit"),
    )

    inherited_attribute_ids = fields.Many2many(
        "product.attribute",
        string="Inherited Attributes",
    )

    # attribute_value_ids = fields.Many2many(
    #     "product.attribute.value",
    #     string="Apply on Variants",
    # )

    # valid_product_attribute_value_wnva_ids = fields.Many2many(
    #     "product.attribute.value",
    #     related="bom_product_id.valid_product_attribute_value_wnva_ids",
    # )

    factor_attribute_id = fields.Many2one(
        "product.attribute",
        string="Factor Attribute",
        help="End product attribute to use for raw material calculation",
    )
    attribute_factor = fields.Float(
        string="Factor", help="Factor to multiply by the numeric value of attribute"
    )

    @api.onchange("product_tmpl_id", "bom_product_id")
    def _product_onchange_domain(self):
        """
        Matched attributes between bom product and product template
        :return: context dict with domain
        """
        vals = []
        if self.product_tmpl_id:
            matched_attributes = self.bom_product_id.mapped(
                "attribute_line_ids.attribute_id"
            ) and self.product_tmpl_id.mapped("attribute_line_ids.attribute_id")
            vals = [
                (
                    "id",
                    "in",
                    matched_attributes.ids,
                )
            ]
        domain = {"domain": {"inherited_attribute_ids": vals}}
        return domain

    def _skip_bom_line(self, product):
        """
        Do not skip bom line if inherited attributes are matched
        """
        self.ensure_one()
        if not self.inherited_attribute_ids or not self._match_inherited_attributes(
            product
        ):
            return True
        else:
            return False
        # return not self.attribute_value_ids or not self._match_attribute_values(product)

    def _match_inherited_attributes(self, product):
        """Match inherited attributes between bom line and product template"""
        self.ensure_one()
        return list(
            set(self.inherited_attribute_ids.ids)
            & set(product.mapped("attribute_value_ids.attribute_id.id"))
        )

    def _match_possible_variant(self, product):
        """Match attribute values as much as possible between bom line and product"""
        self.ensure_one()

        def match_products(products, attr_val_list):
            """Recursive function to match attribute values"""
            if not attr_val_list:
                return products
            attr_val = attr_val_list[0]
            return match_products(
                products.filtered(lambda p: attr_val in p.attribute_value_ids),
                attr_val_list[1:],
            )

        target_products = self.mapped("product_tmpl_id.product_variant_ids")

        # Phase 1: match inherited attributes
        common_attrs = product.attribute_value_ids.filtered(
            lambda a: a.attribute_id in self.inherited_attribute_ids
        )
        if not common_attrs:
            return False
        matched_products = match_products(target_products, common_attrs)
        if not matched_products:
            return False

        # Phase 2: match additional attributes
        line_attribute_ids = self.mapped(
            "product_tmpl_id.attribute_line_ids.attribute_id"
        )
        additional_attr_vals = product.attribute_value_ids.filtered(
            lambda a: a.attribute_id in line_attribute_ids and a not in common_attrs
        )
        matched_products = match_products(matched_products, additional_attr_vals)

        # return single product if possible
        return fields.first(matched_products) or False
