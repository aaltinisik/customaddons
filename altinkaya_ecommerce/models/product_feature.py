# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
from collections import OrderedDict


class ProductTemplateFeatureLine(models.Model):
    """This model adds feature functionality to products. It's a copy of product.template.attribute.line
    and related to product.attribute. So there some attribute_id fields in this model. It's not a mistake."""

    _name = "product.template.feature.line"
    _description = "Product Feature"
    _rec_name = "feature_id"
    _order = "feature_id, id"

    product_tmpl_id = fields.Many2one(
        "product.template",
        string="Product Template",
        ondelete="cascade",
        required=True,
        index=True,
    )
    feature_id = fields.Many2one(
        "product.attribute",
        string="Feature",
        ondelete="restrict",
        required=True,
        index=True,
    )

    attribute_id = fields.Many2one(
        "product.attribute",
        related="feature_id",
        string="Attribute",
        help="Not a real attribute. It's used on Odoo templates.",
        readonly=True,
        store=True,
    )

    value_ids = fields.Many2many("product.attribute.value", string="Feature Values")
    product_template_value_ids = fields.Many2many(
        "product.template.feature.value",
        string="Product Features Values",
        compute="_set_product_template_value_ids",
        store=False,
    )

    @api.constrains("value_ids", "feature_id")
    def _check_valid_features(self):
        if any(
            not line.value_ids or line.value_ids > line.feature_id.value_ids
            for line in self
        ):
            raise ValidationError(
                _("You cannot use this feature with the following value.")
            )
        return True

    @api.model
    def create(self, values):
        res = super(ProductTemplateFeatureLine, self).create(values)
        res._update_product_template_feature_values()
        return res

    def write(self, values):
        res = super(ProductTemplateFeatureLine, self).write(values)
        self._update_product_template_feature_values()

        if "feature_id" in values:
            # delete remaining product.template.feature.value that are not used on any line
            product_template_feature_values_to_remove = self.env[
                "product.template.feature.value"
            ]
            for product_template in self.mapped("product_tmpl_id"):
                product_template_feature_values_to_remove += (
                    product_template_feature_values_to_remove.search(
                        [
                            ("product_tmpl_id", "=", product_template.id),
                            (
                                "product_feature_value_id",
                                "not in",
                                product_template.feature_line_ids.mapped(
                                    "value_ids"
                                ).ids,
                            ),
                        ]
                    )
                )
            product_template_feature_values_to_remove.unlink()

        return res

    @api.depends("value_ids")
    def _set_product_template_value_ids(self):
        for product_template_feature_line in self:
            product_template_feature_line.product_template_value_ids = self.env[
                "product.template.feature.value"
            ].search(
                [
                    (
                        "product_tmpl_id",
                        "in",
                        product_template_feature_line.product_tmpl_id.ids,
                    ),
                    (
                        "product_feature_value_id",
                        "in",
                        product_template_feature_line.value_ids.ids,
                    ),
                ]
            )

    def unlink(self):
        for product_template_feature_line in self:
            self.env["product.template.feature.value"].search(
                [
                    (
                        "product_tmpl_id",
                        "in",
                        product_template_feature_line.product_tmpl_id.ids,
                    ),
                    (
                        "product_feature_value_id.attribute_id",
                        "in",
                        product_template_feature_line.value_ids.mapped(
                            "attribute_id"
                        ).ids,
                    ),
                ]
            ).unlink()

        return super(ProductTemplateFeatureLine, self).unlink()

    def _update_product_template_feature_values(self):
        """
        Create or unlink product.template.attribute.value based on the attribute lines.
        If the product.attribute.value is removed, remove the corresponding product.template.attribute.value
        If no product.template.attribute.value exists for the newly added product.attribute.value, create it.
        """
        for feature_line in self:
            # All existing product.template.attribute.value for this template
            product_template_feature_values_to_remove = self.env[
                "product.template.feature.value"
            ].search(
                [
                    ("product_tmpl_id", "=", feature_line.product_tmpl_id.id),
                    (
                        "product_feature_value_id.attribute_id",
                        "in",
                        feature_line.value_ids.mapped("attribute_id").ids,
                    ),
                ]
            )
            # All existing product.attribute.value shared by all products
            # eg (Yellow, Red, Blue, Small, Large)
            existing_product_features_values = (
                product_template_feature_values_to_remove.mapped(
                    "product_feature_value_id"
                )
            )

            # Loop on product.attribute.values for the line (eg: Yellow, Red, Blue)
            for product_feature_value in feature_line.value_ids:
                if product_feature_value in existing_product_features_values:
                    # property is already existing: don't touch, remove it from list to avoid unlinking it
                    product_template_feature_values_to_remove = (
                        product_template_feature_values_to_remove.filtered(
                            lambda value: product_feature_value
                            not in value.mapped("product_feature_value_id")
                        )
                    )
                else:
                    # property does not exist: create it
                    self.env["product.template.feature.value"].create(
                        {
                            "product_feature_value_id": product_feature_value.id,
                            "product_tmpl_id": feature_line.product_tmpl_id.id,
                        }
                    )

            # at this point, existing properties can be removed to reflect the modifications on value_ids
            if product_template_feature_values_to_remove:
                product_template_feature_values_to_remove.unlink()

    @api.model
    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        if name and operator in ("=", "ilike", "=ilike", "like", "=like"):
            args = args or []
            domain = [
                "|",
                ("feature_id", operator, name),
                ("value_ids", operator, name),
            ]
            feature_ids = self._search(
                expression.AND([domain, args]),
                limit=limit,
                access_rights_uid=name_get_uid,
            )
            return self.browse(feature_ids).name_get()
        return super(ProductTemplateFeatureLine, self)._name_search(
            name=name,
            args=args,
            operator=operator,
            limit=limit,
            name_get_uid=name_get_uid,
        )


class ProductTemplateFeatureValue(models.Model):
    """Materialized relationship between feature values
    and product template generated by the product.template.feature.line"""

    _name = "product.template.feature.value"
    _order = "product_feature_value_id, id"
    _description = "Product Feature Value"

    name = fields.Char("Value", related="product_feature_value_id.name")
    product_feature_value_id = fields.Many2one(
        "product.attribute.value",
        string="Feature Value",
        required=True,
        ondelete="cascade",
        index=True,
    )
    product_tmpl_id = fields.Many2one(
        "product.template",
        string="Product Template",
        required=True,
        ondelete="cascade",
        index=True,
    )
    feature_id = fields.Many2one(
        "product.attribute",
        string="Feature",
        related="product_feature_value_id.attribute_id",
    )
    sequence = fields.Integer("Sequence", related="product_feature_value_id.sequence")

    def name_get(self):
        return [
            (value.id, "%s: %s" % (value.feature_id.name, value.name)) for value in self
        ]

    def _only_active(self):
        return self
