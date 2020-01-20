# -*- coding: utf-8 -*-

{
    'name' : 'Product Harmonized System Code',
    'version' : '12.0.0.0.1',
    'category': 'General',
    'depends' : [
        'product',
        'account',
        'sale',
        'sale_stock',

    ],
    'author' : 'OnurUgur,Codequarters,Ahmet Altınışık',
    'description': """Add hscode for related product categories""",
    'website': 'http://www.altinkaya.eu',
    'data': [
        'security/ir.model.access.csv',
        'views/hscode_view.xml',
        'views/product_category_view.xml',

    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
