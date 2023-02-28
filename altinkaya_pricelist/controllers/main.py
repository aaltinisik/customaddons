# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields
from odoo.http import request, route
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):
    def _get_pricelist(self, pricelist_id, pricelist_fallback=False):
        return request.env["product.pricelist"].browse(int(pricelist_id or 0))

    @route(
        ["/sale/get_combination_pricelist_info"],
        type="json",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def render_pricelist(self, **post):
        pricelist = False
        pricelist_content = []

        if request.env.context.get("website_id"):
            current_website = request.env["website"].get_current_website()
            if not pricelist:
                pricelist = current_website.get_current_pricelist()

        if pricelist and post and post.get("product_id"):
            product_id = post.get("product_id")
            product = request.env["product.product"].sudo().browse(int(product_id))
            price_scales = product.categ_id.pricelist_discount_scales
            if not price_scales:
                return False
            price_scales = [int(x) for x in price_scales.split(",")]
            for idx, scale in enumerate(price_scales):
                price = pricelist._compute_price_rule(
                    product, scale, uom=product.uom_id, date=fields.Datetime.now()
                )
                if price:
                    start = price_scales[idx - 1] if idx > 0 else 1

                    pricelist_content.append(
                        {
                            "qty": "%s - %s" % (start, price_scales[idx]),
                            "price": round(price[product.id][0], 2),
                        }
                    )
            request.env["ir.ui.view"].clear_caches()
            table_html = (
                request.env["ir.ui.view"]
                .with_context(lang=request.env.context.get("lang") or "tr_TR")
                ._render_template(
                    "altinkaya_pricelist.product_price_table_html",
                    {
                        "pricelist_content": pricelist_content,
                        "currency_id": pricelist.currency_id,
                    },
                )
            )
            return {"table_html": table_html}
        return True