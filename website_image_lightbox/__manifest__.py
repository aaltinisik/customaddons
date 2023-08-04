# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Image Lightbox",
    "summary": "Adds lightbox to product images on website",
    "description": "Adds lightbox to product images on website.",
    "development_status": "Beta",
    "version": "16.0.1.0.1",
    "author": "Yiğit Budak",
    "license": "AGPL-3",
    "website": "https://github.com/yibudak",
    "category": "Extensions",
    "depends": ["website", "website_sale"],
    "data": [
        # TEMPLATE
        "templates/product_image_lightbox.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_image_lightbox/static/src/css/lightbox.css",
            "website_image_lightbox/static/src/js/lightbox.js",
        ],
    },
    "installable": True,
}
