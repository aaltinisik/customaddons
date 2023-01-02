# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Altinkaya E-commerce Extensions",
    "summary": "Product and sale e-commerce fields",
    "description": "Bu modul ne yapar #TODO",
    "development_status": "Beta",
    "version": "12.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["product", "product_variant_configurator"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_attribute_view.xml",
        "views/product_template_view.xml",
        "views/product_product_view.xml",
        "views/product_category_view.xml",
    ],
    "installable": True,
}
