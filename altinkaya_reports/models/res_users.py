

from odoo import models,fields,api




class ResUsers(models.Model):
    _inherit='res.users'
    context_def_label_printer = fields.Many2one('printing.printer', string='Default Label Printer')
