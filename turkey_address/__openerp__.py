#Custome Module for Ahmet 
{
    'name': 'Turkey Address',
    'version': '8.0.1',
    'summary': "Add custome field in Customer like District, Resion, Neighbourhood",
    'description': """This Module is used to add custom field in res.partner Object""",
    'category': 'Sale',
    'author': 'Kirankumar',
    'depends': ['sale'],
    'data': [
        'res_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
