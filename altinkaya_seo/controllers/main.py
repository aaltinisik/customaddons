# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website.controllers.main import Website
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.altinkaya_seo.models.ir_http import slug
from odoo import http
from odoo.http import request


class WebsiteSaleSEOInherit(WebsiteSale):
    def sitemap_categories(env, rule, qs):
        if not qs or qs.lower() in "/urunler":
            yield {"loc": "/urunler"}

        Category = env["product.public.category"]
        dom = sitemap_qs2dom(qs, "/urunler", Category._rec_name)
        dom += env["website"].get_current_website().website_domain()
        dom += [("is_published", "=", True)]
        for cat in Category.search(dom):
            loc = "/urunler/%s" % slug(cat)
            if not qs or qs.lower() in loc:
                yield {"loc": loc}

    def sitemap_products(env, rule, qs):
        Products = env["product.template"]
        dom = sitemap_qs2dom(qs, "/urunler", Products._rec_name)
        dom += env["website"].get_current_website().website_domain()
        dom += [
            ("is_published", "=", True),
            ("public_categ_ids", "!=", False),
            ("public_categ_ids.is_published", "=", True),
        ]
        for product in Products.search(dom):
            yield {"loc": product.website_url}

    @http.route(
        ["/urunler/<string:category_seo_name>/<string:product_seo_name>"],
        type="http",
        auth="public",
        website=True,
        sitemap=sitemap_products,
    )
    def seo_product(
        self, category_seo_name, product_seo_name, category="", search="", **kwargs
    ):
        category = (
            request.env["product.public.category"]
            .sudo()
            .search(
                [
                    ("seo_name", "=", category_seo_name),
                    ("is_published", "=", True),
                ],
                limit=1,
            )
        )
        product = (
            request.env["product.template"]
            .sudo()
            .search(
                [
                    ("seo_name", "=", product_seo_name),
                    ("public_categ_ids", "in", category.id),
                    ("is_published", "=", True),
                ],
                limit=1,
            )
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
            "/urunler/page/<int:page>",
            "/urunler/<string:category_seo_name>",
            "/urunler/<string:category_seo_name>/page/<int:page>",
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=sitemap_categories,
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
                .search(
                    [
                        ("seo_name", "=", category_seo_name),
                        ("is_published", "=", True),
                    ],
                    limit=1,
                )
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

    ##### Override for SEO #####
    @http.route(
        [
            "/shop",
            "/shop/page/<int:page>",
            '/shop/category/<model("product.public.category"):category>',
            '/shop/category/<model("product.public.category"):category>/page/<int:page>',
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def shop(
        self,
        page=0,
        category=None,
        search="",
        min_price=0.0,
        max_price=0.0,
        ppg=False,
        **post
    ):
        return super(WebsiteSaleSEOInherit, self).shop(
            page=page,
            category=category,
            search=search,
            min_price=min_price,
            max_price=max_price,
            ppg=ppg,
            **post
        )

    @http.route(
        ['/shop/<model("product.template"):product>'],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def product(self, product, category="", search="", **kwargs):
        return super(WebsiteSaleSEOInherit, self).product(
            product, category, search, **kwargs
        )


class WebsiteInherit(Website):
    @http.route(
        "/website/info", type="http", auth="public", website=True, sitemap=False
    )
    def website_info(self, **kwargs):
        return super(WebsiteInherit, self).website_info(**kwargs)
