# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Website Cart Multi Currency",
    "summary": "Show company currency value and rate in cart",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["website_sale", "website_sale_delivery"],
    "data": [
        "data/data.xml",
        "templates/cart_total_currency.xml",
        "templates/sale_confirmation_amount.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_cart_multi_currency/static/src/js/website_sale_delivery.js",
        ],
    },
    "installable": True,
}
