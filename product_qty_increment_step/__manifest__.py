# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product Qty Increment Step",
    "summary": "Product Qty Increment Step",
    "description": "This module allows you to set a step for product "
                   "quantity increment in the product page.",
    "development_status": "Beta",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["website", "website_sale", "altinkaya_ecommerce"],
    "data": [
        "views/product_template_view.xml",
        "templates/product_quantity.xml"
    ],
    "assets": {
        "web.assets_frontend": [
            "product_qty_increment_step/static/src/js/qty_increment_step.js",
        ],
    },
    "installable": True,
}
