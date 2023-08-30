# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Advanced Faceted Search",
    "summary": "Website advanced faceted search extension.",
    "description": "This module extends Odoo's faceted search.",
    "development_status": "Beta",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["website_sale", "altinkaya_ecommerce"],
    "data": [
        "templates/filter_available_values.xml",
    ],
    "installable": True,
}
