
{
    'name': 'Partner Worksector',
    'version': '12.0',
    'website': 'https://www.codequarters.com',
    'author':'OnurUgur,Codequarters',
    'category': 'Sales',
    'summary': 'add Partner Product relation with sector',
    'description': """
	 """,
    'depends': [
        'sale', 'crm',
    ],
    'data': [
            'security/ir.model.access.csv',
            'views/partner_view.xml',
    ],
    'installable' : True,
    'auto_install' : False,
}
