# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Debug Restrict",
    "summary": "Restrict debug mode for non-admin users",
    "description": "This module:"
                   " - Disables debug mode for non-admin users"
                   " - Hides traceback message for normal users",
    "development_status": "Beta",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["base", "web", "website"],
    "data": [
        "security/res_users.xml",
        # TEMPLATE
        # "templates/cross_selling_on_all_products.xml",
    ],
    "installable": True,
}
