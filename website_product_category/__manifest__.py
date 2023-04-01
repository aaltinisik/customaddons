# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Product Category",
    "summary": "Add description to product category",
    "description": "This module adds description to product category.",
    "development_status": "Beta",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["website", "website_sale"],
    "data": [
        "views/product_public_category_view.xml",
        "templates/product_category_description.xml",
    ],
    # "assets": {
    #     "web.assets_frontend": [
    #         "website_product_category/static/src/js/readmore.js",
    #         "website_product_category/static/src/css/readmore.css",
    #     ],
    # },
    "installable": True,
}
