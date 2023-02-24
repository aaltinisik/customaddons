# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api
from odoo.addons.altinkaya_seo.models.ir_http import slug


class ProductTemplate(models.Model):
    _inherit = "product.template"

    seo_name = fields.Char(
        string="SEO Name",
        help="SEO Name for product",
        compute="_compute_seo_name",
        store=True,
    )

    @api.depends("name")
    def _compute_seo_name(self):
        for product in self:
            product.seo_name = slug(product)

    def _compute_website_url(self):
        """Overwrite this method to use custom slug method."""
        super(ProductTemplate, self)._compute_website_url()
        for product in self:
            if product.id:
                product.website_url = "/urunler/%s/%s" % (
                    slug(product.public_categ_ids),
                    slug(product),
                )

    def _get_product_breadcrumb(self):
        """
        This method is used to create product page breadcrumb.
        """

        def _get_parent(category):
            """Recursively get parent categories.
            Actually odoo has `parents_and_self` method that does the same thing.
            """
            if category.parent_id:
                return category.parent_id + _get_parent(category.parent_id)
            return category

        self.ensure_one()
        tmpl_id = self.sudo()
        Categories = self.env["product.public.category"]
        base_categ = fields.first(tmpl_id.public_categ_ids)
        if base_categ:
            Categories |= base_categ
            Categories |= _get_parent(base_categ)

        return reversed(Categories)
