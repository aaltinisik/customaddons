# -*- encoding: utf-8 -*-

{
    'name': 'Procurement Mass Management',
    'version': '0.01',
    'category': 'Inventory',
    'description': ''' This module allows to manage mass procurement actions as per user rights
''',
    'author': 'Kiran Kantesariya',
    'website': '',
    'images': [],
    'depends': [
        'stock',
    ],
    'data': [
        'security/procurement_security.xml',
        'wizard/run_procurement_view.xml',
        'wizard/check_procurement_view.xml',
        'wizard/reconfirm_procurement_view.xml',
        'wizard/cancel_procurement_view.xml'
    ],
    'init': [],
    'demo': [],
    'update': [],
    'test': [],  # YAML files with tests
    'installable': True,
    'application': False,
    'auto_install': False,  # If it's True, the modules will be auto-installed when all dependencies are installed
    'certificate': '',
}
