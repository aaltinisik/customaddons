
{
    'name': 'altinkaya_worksector',
    'version': '8.0',
    'website': 'https://www.odoo.com',
    'category': 'Sales',
    'summary': 'altinkaya_worksector',
    'description': """
	 """,
    'depends': [
        'sale', 'crm'
    ],
    'data': [
            'security/ir.model.access.csv',
            'views/partner_view.xml',
    ],
    'installable' : True,
    'auto_install' : False,
}
