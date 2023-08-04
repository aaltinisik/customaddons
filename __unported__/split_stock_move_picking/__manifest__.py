# -*- coding: utf-8 -*-
{
    'name': 'Split Stock Move Picking',

    'summary': """
       Splits stock.move record in pickings.
       """,

    'description': """
       Splits stock.move record in stock.picking model.
    """,

    'author': "yibudak",

    'website': "https://github.com/yibudak",

    'category': 'Product',

    'version': '12.0.0.1',

    'depends': ['base', 'stock'],

    'data': [
        'wizard/wizard_split_picking_line.xml',
        'views/stock_picking_view.xml',
    ],
}