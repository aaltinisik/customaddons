# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Variant Table",
    "summary": "Select product variants in a table",
    "description": "This module adds a table to the product page"
    " to select product variants.",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["altinkaya_ecommerce", "website_sale"],
    "data": [
        "templates/product_variant_table.xml",
        "views/product_attribute_view.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "product_variant_table/static/src/js/variant_table.js",
            "product_variant_table/static/src/scss/style.scss",
        ],
    },
    "installable": True,
}
