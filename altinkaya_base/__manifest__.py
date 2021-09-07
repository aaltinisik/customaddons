# -*- coding: utf-8 -*-
{
    'name': "Altinkaya Base & Custom View Updates",
    'summary': """
        Includes base module translations and inherited base views.
        """,
    'description': """        
    """,
    'author': "Yavuz Avcı",
    'website': "https://www.altinkaya.com.tr/",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/apps_view_inherit.xml',
        'views/module_tree_view_inherit.xml'
    ],
    'installable': True
}