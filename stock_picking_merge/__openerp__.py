# -*- coding: utf-8 -*-

{
    'name': 'Stock Picking Merge',
    'version': '8.0',
    'website': 'https://www.odoo.com',
    'category': 'Stock',
    'summary': 'Stock Picking Merge',
    'author': 'Kiran Kantesariya, Ahmet Altinisik',
    'description': """
     """,
    'depends': [
        'stock_account', 'document'
    ],
    'data': [
        'security/res_groups.xml',
        'wizard/picking_merge_wiz_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable' : True,
    'auto_install' : False,
}