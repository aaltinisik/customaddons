# Copyright 2023 Yousef Sheta (https://github.com/TrueYouface)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Altinkaya CRM Extension",
    "summary": "Adds tracking and conversion rates to orders.",
    "description": "This is a CRM module made for Altinkaya.",
    "version": "12.0.1.0.0",
    "category": "General",
    "website": "https://github.com/TrueYouface",
    "author": "Yousef Sheta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["crm", "sale"],
    "data": [
        "views/crm_lead_view.xml",
        "views/sale_order_view.xml",
    ],
}
