# -*- coding: utf-8 -*-
{
    "name": "Badge - Menu",
    "summary": "Show Counter badge on Odoo menu",
    "version": "12.0.1",
    "description": """Show Counter badge on Odoo menu""",
    "version" :  "1.0.0",
    "author": "haiduong",
    "maintainer": "haiduong",
    "website": "http://erptoancau.com",
    "images": ["static/description/menu_badge.png"],
    "license" :  "",
    "category": "Tools",
    "depends": [
        "base",
        "web",
    ],
    "data": [
        'views/assets.xml',
    ],
    "qweb": ['static/src/xml/menu.xml'],
    "installable": True,
    "application": True,
}
