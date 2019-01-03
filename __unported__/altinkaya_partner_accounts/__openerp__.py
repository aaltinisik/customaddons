# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    'name' : 'Partner Accounts',
    'version' : '1.1',
    'author' : 'Acespritech Solutions Pvt. Ltd.',
    'category' : 'Account',
    'description' : """Partner Accounts""",
    'website': 'https://www.acespritech.com',
    'depends' : ['base', 'sale','account_accountant'],
    'data': [
#             'demo/account_demo_data.xml',
            'views/partner_account_wizard_view.xml'
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
#     'post_init_hook': 'post_init'
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: