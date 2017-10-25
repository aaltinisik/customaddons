# -*- coding: utf-8 -*-

{
    'name': 'Product Label Print',
    'version': '8.0',
    'website': 'https://www.odoo.com',
    'category': 'Stock',
    'summary': 'Product Label Print',
    'author': 'Kiran Kantesariya, Ahmet Altinisik',
    'description': """
     """,
    'depends': [
        'report_aeroo', 'product', 'altinkaya_shipment'
    ],
    'data': [
        'wizard/print_pack_barcode_wiz_view.xml',
    ],
    'installable' : True,
    'auto_install' : False,
}
