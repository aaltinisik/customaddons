
{
    'name': 'Partner Import Script ',
    'version': '8.0.2',
    'website': 'https://www.odoo.com',
    'author': 'Kirankumar',
    'category': 'Base',
    'sequence': 14,
    'summary': 'This Module is use to import custom field in res.partner Object using import script',
    'description': """This Module is use to import custom field in res.partner Object""",
    'depends': ['base', 'sale'],
    'data': ['views/wizard_import_script.xml'],
    'installable' : True,
    'auto_install' : False,
}
