
{
    'name': 'Secondary Currency Rate with TCMB',

    'version': '12.0.0.1',

    'website': 'https://github.com/yibudak',

    'author': 'yibudak',

    'category': 'Currency',

    'summary': 'This Module is use to add second rate field to currency rate',

    'description': """This Module is use to add second rate field to currency rate""",

    'depends': ['currency_rate_update', 'currency_rate_update_tcmb'],

    'data': [
        'views/res_currency_view.xml',
        'views/res_currency_rate_view.xml',
        'views/res_currency_rate_provider.xml',
    ],
    'installable' : True,
    'auto_install' : False,
}
