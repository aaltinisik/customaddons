# -*- coding: utf-8 -*-
{
    'name': 'ALTINKAYA MRP Extensions',
    'version': '1.0',
    'author': 'OnurUgur,Dogan ALTUNBAY, CODEQUARTERS',
    'website': 'http://www.codequarters.com',
    'category': 'mrp',
    'sequence': 1,
    'summary': 'Altinkaya MRP module extensions',
    'images': [],
    'depends': ['mrp','stock','sale'],
    'description': """

    """,
    'data': [
        "security/ir.model.access.csv",
        "view/mrp_production_view.xml",
        "view/procurement_view.xml",
        "view/mrp_bom_views.xml",
        'view/x_makine_views.xml',
        'wizard/mrp_cancel_wizard_view.xml',
        'data/data.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
