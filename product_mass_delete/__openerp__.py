# -*- encoding: utf-8 -*-

{
    'name': 'Mass delete Product',
    'version': '0.01',
    'category': 'Inventory',
    'description': ''' Adds a multi action menu to product.product list deleting EAN13 and deleting product skips to next product in case of exception.
''',
    'author': 'Ahmet Altinisik',
    'website': '',
    'images': [],
    'depends': [
        'stock',
    ],
    'data': [
        'security/mass_delete.xml',
        'wizard/mass_delete_view.xml',
    ],
    'init': [],
    'demo': [],
    'update': [],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'certificate': '',
}
