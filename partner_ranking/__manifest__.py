
{
    'name': 'Partner Ranking with Sale',
    'version': '12.0.1',
    'website': 'https://www.codequarters.com',
    'category': 'Sales',
    'summary': 'Altinkaya Partner Ranking',
    'description': """
	 """,
    'depends': [
        'partner_worksector'
    ],
    'data': [
            'data/scheduler_notification.xml',
            'views/res_partner_view.xml',
            'views/product_product_view.xml',
            'views/stock_warehouse_orderpoint_view.xml',

    ],
    'installable' : True,
    'auto_install' : False,
}
