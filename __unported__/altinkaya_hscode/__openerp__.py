# -*- coding: utf-8 -*-

{
    'name' : 'Altinkaya hscode',
    'version' : '1.0',
    'category': 'General',
    'depends' : [
        'product',
        'account',
        'sale',
        'sale_stock',

    ],
    'author' : 'Ahmet Altınışık',
    'description': """Add hscode for related product categories""",
    'website': 'http://www.altinkaya.eu',
    'data': [
        'hscode_view.xml',
        'product_category_view.xml',

    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
