# -*- coding: utf-8 -*-
{
    'name': "currency_difference_invoice",

    'summary': """
        This module is for creating invoice with difference currency amount""",

    'description': """
        * Calculate currency difference amount
        * Create an invoice with calculated amount
        
    """,

    'author': "yibudak",
    'website': "https://github.com/yibudak",
    'category': 'Accounting',
    'version': '0.1',

    'depends': ['base', 'account'],

    'data': [
        'views/res_partner_view.xml',
        'views/res_company_view.xml',
        'views/account_invoice_view.xml',
        'wizard/create_currency_difference_invoices.xml',
    ],
}
