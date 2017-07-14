
{
    'name': 'Account Invoice in Turkey currency ',
    'version': '8.0.2',
    'website': 'https://www.odoo.com',
    'author': 'Kirankumar',
    'category': 'Invoice',
    'summary': 'This Module is used to calculate total invoice amount in turkey currency',
    'description': """This Module is use to Export Invoice""",
    'depends': ['base', 'account_accountant'],
    'installable' : True,
    'auto_install' : False,
    'data': [
             'views/account_invoice_view.xml',
             ],
}


