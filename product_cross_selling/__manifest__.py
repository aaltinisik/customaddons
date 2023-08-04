# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product Cross Selling",
    "summary": "Cross selling products for each product",
    "description": "This module automatically finds cross selling products for each product",
    "development_status": "Beta",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["website", "website_sale"],
    "data": [
        # TEMPLATE
        "templates/cross_selling_on_all_products.xml",
    ],
    "installable": True,
}
