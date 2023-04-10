# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product Previous Next",
    "summary": "Walk through products with next and previous buttons",
    "description": "This module adds next and previous buttons to product page",
    "development_status": "Beta",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["website_sale"],
    "data": [
        "templates/previous_next_buttons.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "product_previous_next/static/src/css/navigation_button.css",
        ],
    },
    "installable": True,
}
