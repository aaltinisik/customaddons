
{
    'name': 'Altinkaya Warehouse',
    'version': '1.1',
    'author': 'Kiran Kantesariya',
    'category': 'Stock',
    'description': """This Module is used to print a stock report""",
    'summary': '',
    'website': '',
    'depends': ['base','stock','mrp'],
    'data': [
             'views/product_view.xml',
             'views/report_stockpicking.xml',
             ],
    'installable': True,
    'auto_install': False
}


