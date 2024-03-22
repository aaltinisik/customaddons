# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Altinkaya Purchase Order Extensions',
    'version': '12.0',
    'category': 'General',
    'depends': ['base', 'purchase', 'stock'],
    'author': 'Yiğit Budak',
    'description': """
    Purchase Order Customization
    """,
    'website': 'https://github.com/yibudak',
    'data': [
        'views/purchase_order_views.xml',
        'views/product_views.xml',
        'views/res_partner_views.xml',
        'views/procurement_group_views.xml',
    ],
    'installable': True,
    'auto_install': False,

}
