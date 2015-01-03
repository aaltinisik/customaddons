{
    'name': 'Socket IO',
    'version': '1.0.0',
    'sequence': 150,
    'category': 'Anybox',
    'description': """""",
    'author': 'ANYBOX',
    'website': 'www.anybox.fr',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'js': [
        'static/lib/js/socket.io.js',
        'static/src/js/socket.io.js',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
