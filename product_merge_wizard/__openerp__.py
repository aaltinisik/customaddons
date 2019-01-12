# -*- encoding: utf-8 -*-
{
    'name' : 'Product Merge Wizard',
    'author' : 'CODEQUARTERS',
    'website' : "http://www.codequarters.com",
    'version' : "1.0",
    'depends' : ['product'],
    'description': """
	This module introduces a wizard to merge products in a single template.
	""",        
    'category' : 'Tools',
    'data': ['security/res_groups.xml',
             'wizard/product_merge_wizard.xml',
             'wizard/product_move_wizard.xml',
             'security/ir.model.access.csv'],
    'demo': [],
    'test': [],
    'installable': True,

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

