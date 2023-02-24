# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.altinkaya_seo.models.ir_http import slug
from odoo import http
from odoo.http import request


class WebsiteSaleSEOInherit(WebsiteSale):
    def sitemap_shop(env, rule, qs):
        if not qs or qs.lower() in "/shop":
            yield {"loc": "/shop"}

        Category = env["product.public.category"]
        dom = sitemap_qs2dom(qs, "/shop/category", Category._rec_name)
        dom += env["website"].get_current_website().website_domain()
        for cat in Category.search(dom):
            loc = "/shop/category/%s" % slug(cat)
            if not qs or qs.lower() in loc:
                yield {"loc": loc}

    @http.route(
        ["/urunler/<string:category_seo_name>/<string:product_seo_name>"],
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def seo_product(
        self, category_seo_name, product_seo_name, category="", search="", **kwargs
    ):
        category = (
            request.env["product.public.category"]
            .sudo()
            .search([("seo_name", "=", category_seo_name)], limit=1)
        )
        product = (
            request.env["product.template"]
            .sudo()
            .search([("seo_name", "=", product_seo_name)], limit=1)
        )
        if not (product and category):
            return request.not_found()

        return request.render(
            "website_sale.product",
            self._prepare_product_values(product, category, search, **kwargs),
        )

    @http.route(
        [
            "/urunler",
            "/urunler/sayfa/<int:page>",
            "/urunler/<string:category_seo_name>",
            "/urunler/<string:category_seo_name>/sayfa/<int:page>",
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=sitemap_shop,
    )
    def seo_shop(
        self,
        page=0,
        category_seo_name=None,
        search="",
        min_price=0.0,
        max_price=0.0,
        ppg=False,
        **post
    ):
        category = request.env["product.public.category"]
        if category_seo_name:
            category = (
                request.env["product.public.category"]
                .sudo()
                .search([("seo_name", "=", category_seo_name)], limit=1)
            )
            if not category:
                return request.not_found()

        return super(WebsiteSaleSEOInherit, self).shop(
            page=page,
            category=category,
            search=search,
            min_price=min_price,
            max_price=max_price,
            ppg=ppg,
            **post
        )
