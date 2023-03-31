# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController


class WebsiteAltinkayaVariantController(WebsiteSaleVariantController):
    @http.route()
    def get_combination_info_website(
        self, product_template_id, product_id, combination, add_qty, **kw
    ):
        res = super(
            WebsiteAltinkayaVariantController, self
        ).get_combination_info_website(
            product_template_id, product_id, combination, add_qty, **kw
        )
        if res.get("product_id"):
            product = request.env["product.product"].browse(res["product_id"])
            res["default_code"] = product.default_code or ""
            res["barcode"] = product.barcode or ""
        return res
