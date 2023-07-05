# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Debug Restrict",
    "summary": "Restrict debug mode for non-admin users",
    "description": "This module:"
    " - Hides traceback message for unauthorized users",
    "development_status": "Beta",
    "version": "12.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["base", "web"],
    "data": [
        "security/res_users.xml",
    ],
    "installable": True,
}
