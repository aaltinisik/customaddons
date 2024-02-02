# Copyright 2020 Yiğit Budak (https://github.com/yibudak)
# Copyright 2019 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Currency Rate Update: Turkish Central Bank',
    'version': '12.0.1.0.0',
    'category': 'Financial Management/Configuration',
    'summary': 'Update exchange rates using TCMB.gov.tr',
    'author':
        'Yiğit Budak, '
        'Odoo Community Association (OCA)',
        'Brainbean Apps'
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'depends': [
        'currency_rate_update',
    ],
    'data': [
        'views/res_currency_rate_provider.xml',
    ],
}
