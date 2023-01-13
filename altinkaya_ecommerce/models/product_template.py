# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from collections import OrderedDict
from odoo import fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_published = fields.Boolean(
        string="Is Published",
        help="If checked, the product will be published on the website.",
        default=False,
    )

    public_description = fields.Html(
        "Description for e-Commerce",
        sanitize_attributes=False,
        translate=False,
        copy=False,
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

    def _prepare_product_attachments_table(self):
        """This method returns product attachments."""
        attachments = self.sudo().website_attachment_ids
        return attachments

    # def price_compute(
    #     self, price_type, uom=None, currency=None, company=None, date=False
    # ):
    #     """Override price_compute method to use sale_price field."""
    #     res = super(ProductTemplate, self).price_compute(
    #         "sale_price", uom=uom, currency=currency, company=company, date=date
    #     )
    #     return res
    # NOTE: price field is missing. You need to add sale_price to template


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

    def _prepare_categories_for_display(self):
        """
        This method adds feature lines to the product specifications.
        """
        res = super(
            ProductTemplateAttributeLine, self
        )._prepare_categories_for_display()
        ptal = res.get(self.env["product.attribute.category"], False)
        res[self.env["product.attribute.category"]] = []
        if ptal:
            tmpl_id = ptal[0].product_tmpl_id.sudo()
            #  Attributes first
            for line in ptal.filtered(lambda x: len(x.value_ids) > 0):
                res[self.env["product.attribute.category"]].append(line)

            ptfl = tmpl_id.feature_line_ids
            for line in ptfl.filtered(lambda x: len(x.value_ids) > 0):
                res[self.env["product.attribute.category"]].append(line)

        return res
