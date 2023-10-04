# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.website_sale_delivery.controllers.main import WebsiteSaleDelivery
from odoo.http import request


class WebsiteSaleDeliveryInherit(WebsiteSaleDelivery):
    def _update_website_sale_delivery_return(self, order, **post):
        """
        Inherited to update amount_currency when delivery method is changed.
        """
        res = super()._update_website_sale_delivery_return(order, **post)
        Monetary = request.env["ir.qweb.field.monetary"]
        if order.currency_id != order.company_currency_id:
            res.update(
                {
                    "new_amount_total_company_currency": Monetary.value_to_html(
                        order.amount_total_company_currency,
                        {"display_currency": order.company_currency_id},
                    ),
                }
            )
        return res
