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
    'name' : 'Partner Analysis',
    'version' : '1.1',
    'author' : 'Acespritech Solutions Pvt. Ltd.',
    'category' : 'Account',
    'description' : """Partner Analysis""",
    'website': 'https://www.acespritech.com',
    'depends' : ['base', 'sale','account_accountant'],
    'data': [
        'security/security.xml',
        'views/account_invoice_report_view.xml',
        'views/partner_view.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
#     'post_init_hook': 'post_init'
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: