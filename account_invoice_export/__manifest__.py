
{
    'name': 'Account Invoice in Turkish Lira',
    'version': '12.0.0.1',
    'website': 'https://altinkaya.com.tr',
    'author': 'Yiğit Budak, Kirankumar',
    'category': 'Invoice',
    'summary': 'This Module is used to calculate total invoice amount in Turkish Lira',
    'description': """This Module is use to Export Invoice""",
    'depends': ['base','account'],
    'installable' : True,
    'auto_install' : False,
    'data': [
             'views/account_invoice_view.xml',
             ],
}


