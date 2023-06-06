# Copyright 2023 Samet Altuntaş (https://github.com/samettal)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Altinkaya Nace Extension",
    "summary": "Adds a button that lists all partners related to particular nace.",
    "description": "This module adds a 'Partners' button to the NACE record form in Odoo, instantly displaying all associated partners in a convenient list view upon click.",
    "version": "12.0.1.0.0",
    "category": "General",
    "website": "https://github.com/samettal",
    "author": "Samet Altuntaş",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["l10n_eu_nace"],
    "data": [
        "views/nace_form_view.xml",
    ],
}
