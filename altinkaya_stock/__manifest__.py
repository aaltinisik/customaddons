{
    'name': 'Altinkaya Stock',
    'version': '12.0',
    'website': 'https://www.altinkaya.com.tr',
    'author':'Ahmet Altınışık,OnurUgur,Codequarters',
    'category': 'Stock',
    'summary': 'add specialized stock extensions',
    'description': """
     """,
    'depends': [
        'stock','delivery'
    ],
    'data': [
            'views/stock_picking_views.xml',
            'views/stock_view.xml',
            'views/delivery_carrier_views.xml',
    ],
    'installable' : True,
    'auto_install' : False,
}
