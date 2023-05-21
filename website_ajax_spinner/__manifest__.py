# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Ajax Spinner",
    "summary": "Show spinner when ajax request is processing",
    "description": "This module shows spinner when ajax request is processing.",
    "development_status": "Beta",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["website"],
    "data": [
        # TEMPLATE
        "templates/website_spinner.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_ajax_spinner/static/src/js/ajax_spinner.js",
            "website_ajax_spinner/static/src/scss/spinner.scss",
        ],
    },
    "installable": True,
}
