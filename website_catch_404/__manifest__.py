# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Catch 404 Errors",
    "summary": "Catch All 404 Errors and Log Them",
    "description": "This module is developed to handle 404 errors."
                   " It logs all 404 errors and shows them in the backend."
                   " When any product or category is renamed,"
                   " it will automatically adds redirections to the new url.",
    "development_status": "Beta",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["website"],
    "data": [
        "security/ir.model.access.csv",
        "views/website_views.xml",
        "views/website_404_errors_views.xml",
        "views/website_rewrite_views.xml",
    ],
    "installable": True,
}
