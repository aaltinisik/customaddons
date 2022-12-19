# -*- coding: utf-8 -*-
{
    'name': "Altinkaya Base & Custom View Updates",
    'summary': """
        Includes base module translations and inherited base views.
        """,
    'description': """        
    """,
    'author': "Yavuz Avcı, Yiğit Budak",
    'website': "https://www.altinkaya.com.tr/",
    'category': 'Web',
    'version': '0.1',

    'depends': ['base', 'web', 'product', 'stock', 'sale', 'account', 'partner_ranking', 'altinkaya_stock', 'mrp',
                'purchase'],

    'data': [
        'views/uom_widget_views.xml',
    ],
    'installable': True
}
