{
    'name' : 'Create invoice from deliveries',
    'version' : '11.0',
    'author' : 'CODEQUARTERS',
    'summary': 'Adds functionality to create invoice from deliveries',
    'description': """
""",
    'website': 'https://www.codequarters.com',
    'depends' : [
        'stock', 'account', 'sale', 'purchase'
        ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/picking_create_invoice_view.xml',
        'views/stock_picking_view.xml',
        'views/account_views.xml'
    ],
    'installable': True,
    'auto_install': False,
}
