# -*- coding: utf-8 -*-


{
    'name': 'Print waybill for pickings',
    'version': '1.0',
    'category': 'Warehouse',
    'summary': 'Adds waybill print function to stock pickings',
    'description': """
    """,
    'author': 'yibudak',
    'website': 'http://www.altinkaya.com.tr',
    'depends': ['stock'],
    'data': [
        'views/stock_warehouse_view.xml',
        'wizard/print_waybill_wizard.xml',
        'report/waybill_reports.xml',
        'report/reports.xml',
    ],
    'installable': True,
}