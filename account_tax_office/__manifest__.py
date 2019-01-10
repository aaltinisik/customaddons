{
    'name': 'Tax Office',
    'version': '1.0',
    'category': 'Account',
    'summary': 'Adds tax office management',
    'description': """
Tax Office
====================================================

Adds tax office management and selection of tax office (along with tax id. number).

Türkiye'de vergi dairesi alanı için kullanılır.

    """,
    'author': 'Codequarters',
    'website': 'http://www.codequarters.com',
    'depends': ['base', 'account'],
    'data': [
        'views/tax_office_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
