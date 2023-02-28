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
        """Overwrite this method to use custom slug method.
        NOTE: Only compute website url for published products.
        """
        super(ProductTemplate, self)._compute_website_url()
        for product in self:
            if product.id and product.is_published and product.public_categ_ids:
                category = fields.first(product.public_categ_ids)
                product.website_url = "/urunler/%s/%s" % (
                    slug(category),
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

    @api.model
    def _search_get_detail(self, website, order, options):
        """
        Overwrite this method to add `is_published` filter to base domain.
        Todo yigit: maybe we don't need this method anymore.
        """
        res = super(ProductTemplate, self)._search_get_detail(website, order, options)
        if res and "base_domain" in res:
            res["base_domain"] += [[("is_published", "=", True), ("categ_id.is_published", "=", True)]]
        return res