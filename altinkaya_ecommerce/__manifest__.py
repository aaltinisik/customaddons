# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Altinkaya E-commerce Extensions",
    "summary": "Product and sale e-commerce fields",
    "description": "Bu modul ne yapar #TODO",
    "development_status": "Beta",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["product", "connector_odoo"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_attribute_view.xml",
        "views/product_template_view.xml",
        "views/product_product_view.xml",
    ],
    "installable": True,
}
