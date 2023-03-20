# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Altinkaya Website SEO Extensions",
    "summary": "This module provides SEO improvements for e-commerce website",
    "description": "This module provides SEO improvements for e-commerce website",
    "development_status": "Beta",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["http_routing", "website", "website_sale"],
    "data": [
        "views/ir_ui_view_views.xml",
        # TEMPLATES
        "templates/view_pages_title.xml",
        "templates/product_breadcrumb_full.xml",
        "templates/grid_breadcrumb.xml",
        "templates/shop_category_title.xml",
        "templates/product_categories_list.xml",
        "templates/categorie_link.xml",
        "templates/general_views.xml",
    ],
    "installable": True,
}
