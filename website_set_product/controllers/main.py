# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):
    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        fuzzy_search_term, product_count, search_result = super(
            WebsiteSaleInherit, self
        )._shop_lookup_products(attrib_set, options, post, search, website)

        if search_result:
            search_result = search_result.filtered(lambda p: not p.sub_component)

        return fuzzy_search_term, product_count, search_result
