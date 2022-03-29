# -*- coding: utf-8 -*-
{
    'name': "change_partner_accounts",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        This module:
        * adds main currency of payment in invoice forms widget
        
    """,

    'author': "yibudak",
    'website': "https://github.com/yibudak",
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/change_partner_accounts_usd_view.xml',
        'wizard/change_partner_accounts_try_view.xml',
        'wizard/change_partner_accounts_eur_view.xml',
    ],
}