# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Sale Schema Fix",
    "summary": "Google Search Console Schema Errors Fix",
    "description": "This module adds missing schema.org markup to the product page.",
    "development_status": "Beta",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["website", "website_sale"],
    "data": [
        # TEMPLATE
        # "templates/cross_selling_on_all_products.xml",
        "templates/product_schema_markup.xml",
        "views/website_views.xml",
    ],
    "installable": True,
}
