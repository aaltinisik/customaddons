
{
    'name': 'altinkaya_partner_ranking',
    'version': '8.0.1',
    'website': 'https://www.odoo.com',
    'category': 'Sales',
    'summary': 'Altinkaya Partner Ranking',
    'description': """
	 """,
    'depends': [
        'altinkaya_worksector'
    ],
    'data': [
            'data/scheduler_notification.xml',
            'views/res_partner_view.xml',
    ],
    'installable' : True,
    'auto_install' : False,
}
