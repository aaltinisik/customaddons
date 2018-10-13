{
    'name': 'Altinkaya Warehouse',
    'version': '1.1',
    'author': 'Kiran Kantesariya, Dogan Altunbay',
    'category': 'Stock',
    'description': """This Module is used to print a stock report""",
    'summary': '',
    'website': '',
    'depends': ['stock'],
    'data': [
             'views/procurement_view.xml',
             'views/stock_location_view.xml',
             'views/stock_move_view.xml',
             'views/stock_picking_despatch_view.xml',
             'wizard/wizard_create_despatch_view.xml',
             'report/report_location_barcode.xml',
             'report/report_picking_despatch.xml'
             ],
    'installable': True,
    'auto_install': False
}


