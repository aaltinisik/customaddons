# -*- coding: utf-8 -*-
# © 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Multiple Images in Products",
    "version": "8.0.2.0.1",
    "author": "Codequarters - Dogan Altunbay",
    "license": "AGPL-3",
    "website": "http://www.codequarters.com",
    "category": "Extensions",
    "depends": [
        "product",
    ],
    "data": [
        'views/product_template_view.xml',
        'views/web_assets.xml'
    ],
    'qweb':[
        'static/src/xml/image_galery_templates.xml',
        ],
    'installable': True,

}
