{
    'name' : 'Altinkaya Security Roles&Rules',
    'version' : '12.0',
    'category': 'General',
    'author' : 'MAkifOzdemir,Codequarters',
    'description': """
    Altınkaya Roles
    """,
    'website': 'http://www.codequarters.com',
     'depends' : ['sale', 'sales_team', 'crm','sale_cancel_reason'],
    'data': [
            'data/altinkaya_category_data.xml',
            'security/altinkaya_security.xml',
            'security/ir.model.access.csv',
            'views/res_users.xml',
            ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    
}
