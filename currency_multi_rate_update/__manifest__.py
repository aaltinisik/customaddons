# -*- coding: utf-8 -*-
# © 2008-2016 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Currency Multi Rate Update",
    "version": "10.0.1.0.0",
    "author": "Camptocamp,Odoo Community Association (OCA)",
    "website": "http://www.codequarters.com",
    "license": "AGPL-3",
    "category": "Financial Management/Configuration",
    "depends": [
        "base",
        "account",  # Added to ensure account security groups are present
        "currency_rate_type"
    ],
    "data": [
        "data/cron.xml",
        "views/company_view.xml",
        "views/currency_rate_update.xml",
        "views/res_config_settings_views.xml",
        "security/rule.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True
}
