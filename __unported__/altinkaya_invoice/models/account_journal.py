'''
Created on Feb 14, 2020

@author: cq
'''
from odoo import fields,models

class AccountJournal(models.Model):
    _inherit = "account.journal"

    name = fields.Char(string='Journal Name', required=True,translate=True)