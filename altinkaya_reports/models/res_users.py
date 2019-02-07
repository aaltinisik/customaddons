

from odoo import models,fields,api




class ResUsers(models.Model):
    _inherit='res.users'
    
    
    
    context_def_label_printer = fields.Char(
        string='Default Label Printer',
        help="",
        required=False,
        company_dependent=True)
