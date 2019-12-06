# -*- coding: utf-8 -*-
{
    'name': 'Purchase Order Excel',
    'version': '1.0.0',
    'category': 'Purchase',
    'summary': '''
        Prints Excel Report based on purchase order status and vendor.
        ''',
    'author': 'HK',
    'license': "OPL-1",
    'depends': [
        'purchase'
    ],
    'data': [
        'wizard/purchase_order_xls_view.xml'
    ],
    'demo': [],  
    'images': ['static/description/banner.png'],
    'auto_install': False,
    'installable': True,
    'application': True
}