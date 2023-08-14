# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.translate import html_translate
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _order = "website_sequence asc, name"

    is_published = fields.Boolean(
        string="Is Published",
        help="If checked, the product will be published on the website.",
        default=False,
    )

    public_description = fields.Html(
        "Description for e-Commerce",
        sanitize_attributes=False,
        translate=html_translate,
        copy=False,
    )

    short_public_description = fields.Text(
        "Short Description for e-Commerce",
        copy=False,
        translate=True,
    )

    website_attachment_ids = fields.Many2many(
        string="Website attachments",
        comodel_name="ir.attachment",
        help="Files publicly downloadable from the product eCommerce page.",
    )

    feature_line_ids = fields.One2many(
        comodel_name="product.template.feature.line",
        inverse_name="product_tmpl_id",
        string="Features",
    )

    website_sequence = fields.Integer(
        "Website Sequence",
        help="Determine the display order in the Website E-commerce",
        default=lambda self: self._default_website_sequence(),
        copy=False,
    )

    set_product = fields.Boolean(
        "Set Product?",
        help="If set, an alert will be shown on the product page.",
    )

    sub_component = fields.Boolean(
        "Sub Component?",
        help="If set, this product will not be shown in the shop.",
    )

    qty_increment_step = fields.Integer(
        string="Qty Increment Step",
        default=1,
        help="Set a step for product quantity increment in the product page."
        " Set 0 to disable this feature.",
    )

    default_variant_id = fields.Many2one(
        comodel_name="product.product",
        string="Default Variant",
        domain="[('product_tmpl_id', '=', id), ('is_published', '=', True)]",
        store=True,
        readonly=False,
    )

    def action_compute_default_variant(self):
        """
        Compute the default variant of the product based on the total sale quantity.
        :return:
        """
        self.ensure_one()
        sales_quant = {
            p.id: p.sales_count
            for p in self.product_variant_ids.filtered(lambda p: p.is_published)
        }
        if sales_quant:
            default_variant = max(sales_quant, key=sales_quant.get)
            self.default_variant_id = default_variant
            _logger.info(
                "Default variant of %s is set to %s",
                self.name,
                self.default_variant_id.display_name,
            )
        else:
            self.default_variant_id = fields.first(self.product_variant_ids)
            _logger.info(
                "No variants found. Default variant of %s is set to %s",
                self.name,
                self.default_variant_id.display_name,
            )
        self.env.cr.commit()
        return True

    def action_open_v16_product_page(self):
        """
        Open the product page in V16.
        :return:
        """
        self.ensure_one()
        base_url = "http://www.altinkaya.com.tr/web/product_v12_redirect?id=%s"
        client_action = {
            "type": "ir.actions.act_url",
            "name": "Product E-commerce Page",
            "target": "new",
            "url": base_url % self.id,
        }
        return client_action

    def _compute_set_products(self):
        phantom_bom = (
            self.env["mrp.bom"]
            .sudo()
            .search([("product_tmpl_id", "in", self.ids), ("type", "=", "phantom")])
        )
        for x in phantom_bom:
            x.product_tmpl_id.set_product = True

    def _compute_sub_component(self):
        """
        Multi record method to check if a product is a subcomponent of a set product.
        """
        query = f"""SELECT p.id, b.type
                    FROM product_template p
                    INNER JOIN (
                      SELECT DISTINCT pp.product_tmpl_id, b.type
                      FROM mrp_bom b
                      INNER JOIN mrp_bom_line bl ON b.id = bl.bom_id
                      INNER JOIN product_product pp ON bl.product_id = pp.id
                      WHERE b.type = 'phantom'
                    ) AS b ON p.id = b.product_tmpl_id
                    WHERE p.id IN %s"""
        self.env.cr.execute(query, (tuple(self.ids),))
        result = self.env.cr.fetchall()
        if result:
            result = set([x[0] for x in result])
            for product in self:
                try:
                    product.sub_component = product.id in result
                except:
                    pass
        else:
            for product in self:
                product.sub_component = False

    def _default_website_sequence(self):
        """
        This method is implemented from Odoo 16.0
        Check the following link for more information:
        https://6sn.de/websitesequence
        """
        self._cr.execute("SELECT MAX(website_sequence) FROM %s" % self._table)
        max_sequence = self._cr.fetchone()[0]
        if max_sequence is None:
            return 10000
        return max_sequence + 5

    @api.multi
    def write(self, vals):
        """Prevent saving attributes with single value."""
        res = super(ProductTemplate, self).write(vals)

        for attr_line in self.mapped(lambda p: p.attribute_line_ids):
            if attr_line.required and len(attr_line.value_ids.ids) < 2:
                raise ValidationError(
                    _(
                        "You can not save required attributes"
                        " with single value. %s " % attr_line.attribute_id.display_name
                    )
                )
        return res

    def action_fill_missing_product_attrs(self):
        """Fill missing product variants for published attribute values."""
        if len(self.product_variant_ids) == 1:
            raise ValidationError(
                _("You can not fill missing product of non variant product.")
            )

        tmpl_attribute_lines = self.attribute_line_ids.filtered(
            lambda x: x.attribute_id.allow_filling
        )
        required_attrs = tmpl_attribute_lines.mapped("attribute_id")
        filled_variant_ids = []

        for product in self.product_variant_ids:
            product_attrs = product.attribute_value_ids.mapped("attribute_id")
            if not all(x in product_attrs.ids for x in required_attrs.ids):
                missing_attrs = required_attrs - product_attrs
                for attr in missing_attrs:
                    tmpl_line = tmpl_attribute_lines.filtered(
                        lambda x: x.attribute_id == attr
                    )
                    default_attr_value = tmpl_line.default_value_id
                    if not default_attr_value:
                        raise ValidationError(
                            _("Set default value for attribute %s" % attr.name)
                        )
                    product.attribute_value_ids |= default_attr_value
                    if (
                        len(
                            self.product_variant_ids.filtered(
                                lambda p: p.attribute_value_ids
                                == product.attribute_value_ids
                            )
                        )
                        > 1
                    ):
                        raise ValidationError(
                            _(
                                "There is already a product with same attribute values. You might do something wrong."
                            )
                        )
                    tmpl_line.value_ids |= default_attr_value
                    filled_variant_ids.append(product.id)

        if not filled_variant_ids:
            raise ValidationError(_("No missing product variants found."))

        tree_view_id = self.env.ref("product.product_product_tree_view").id
        action = {
            "type": "ir.actions.act_window",
            "views": [(tree_view_id, "tree")],
            "view_mode": "tree,form",
            "name": _("Products"),
            "res_model": "product.product",
            "domain": "[('type', '=', 'product'), ('id', 'in', %s)]"
            % filled_variant_ids,
        }
        return action

    def action_list_missing_product_attrs(self):
        """List missing product variants for published attribute values."""
        ProductProduct = self.env["product.product"]
        tmpl_ids = self.env["product.template"].search(
            [
                ("is_published", "=", True),
                ("categ_id.is_published", "=", True),
            ]
        )
        for tmpl in tmpl_ids:
            if tmpl.product_variant_count == 1:
                continue
            attribute_lines = tmpl.attribute_line_ids.filtered(
                lambda x: x.attribute_id.allow_filling
            )
            required_attrs = attribute_lines.mapped("attribute_id")
            for product in tmpl.product_variant_ids:
                product_attrs = product.attribute_value_ids.mapped("attribute_id")
                if not all(x in product_attrs.ids for x in required_attrs.ids):
                    ProductProduct |= product

        tree_view_id = self.env.ref("product.product_product_tree_view").id
        form_view_id = self.env.ref("product.product_normal_form_view").id
        action = {
            "type": "ir.actions.act_window",
            "views": [(tree_view_id, "tree"), (form_view_id, "form")],
            "view_mode": "tree,form",
            "name": _("Attributes Missing Products"),
            "res_model": "product.product",
            "domain": "[('type', '=', 'product'), ('id', 'in', %s)]"
            % ProductProduct.ids,
        }
        return action


class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    default_value_id = fields.Many2one(
        string="Default Value",
        comodel_name="product.attribute.value",
        help="Default value for the attribute.",
    )

    allow_filling = fields.Boolean(
        string="Allow Filling",
        help="If checked, attribute values will be filled automatically",
        related="attribute_id.allow_filling",
        readonly=True,
    )
