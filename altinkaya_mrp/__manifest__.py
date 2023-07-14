# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "ALTINKAYA MRP Extension",
    "summary": "Extra features for MRP Module",
    "description": "This module adds extra features to MRP Module.",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["mrp"],
    "data": [
        "security/ir.model.access.csv",
        "views/mrp_bom_template_line_views.xml",
    ],
    "installable": True,
}
