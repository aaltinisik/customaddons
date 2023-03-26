# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http, fields
from odoo.http import request
from werkzeug.urls import url_decode, url_encode, url_parse
from odoo.addons.altinkaya_seo.models.ir_http import slug


class WebsiteSaleInherit(WebsiteSale):
    @http.route(
        ["/shop/change_pricelist/<string:pricelist_value>"],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def pricelist_change(self, pricelist_value, **post):
        website = request.env["website"].get_current_website()
        pricelist = request.env["product.pricelist"]
        try:
            pricelist_id = int(pricelist_value)
            pricelist = request.env["product.pricelist"].sudo().browse(pricelist_id)
        except ValueError:
            pricelists = request.env["product.pricelist"].sudo().search([])
            for pl in pricelists:
                if slug(pl) == pricelist_value:
                    pricelist = pl
                    break

        redirect_url = request.httprequest.referrer
        if self._check_pricelist_available(website, pricelist):
            if redirect_url and request.website.is_view_active(
                "website_sale.filter_products_price"
            ):
                decoded_url = url_parse(redirect_url)
                args = url_decode(decoded_url.query)
                min_price = args.get("min_price")
                max_price = args.get("max_price")
                if min_price or max_price:
                    previous_price_list = request.website.get_current_pricelist()
                    try:
                        min_price = float(min_price)
                        args["min_price"] = min_price and str(
                            previous_price_list.currency_id._convert(
                                min_price,
                                pricelist.currency_id,
                                request.website.company_id,
                                fields.Date.today(),
                                round=False,
                            )
                        )
                    except (ValueError, TypeError):
                        pass
                    try:
                        max_price = float(max_price)
                        args["max_price"] = max_price and str(
                            previous_price_list.currency_id._convert(
                                max_price,
                                pricelist.currency_id,
                                request.website.company_id,
                                fields.Date.today(),
                                round=False,
                            )
                        )
                    except (ValueError, TypeError):
                        pass
                    redirect_url = decoded_url.replace(query=url_encode(args)).to_url()
            request.session["website_sale_current_pl"] = pricelist.id
            request.website.sale_get_order(update_pricelist=True)
        return request.redirect(redirect_url or "/urunler")

    def _check_pricelist_available(self, website, pricelist):
        """
        Check if pricelist is available for current user.
        """
        if (
            (
                pricelist.selectable
                or pricelist == request.env.user.partner_id.property_product_pricelist
            )
            or request.env.user.partner_id.website_pricelist_id == pricelist
        ) and website.is_pricelist_available(pricelist.id):
            return True

        return False
