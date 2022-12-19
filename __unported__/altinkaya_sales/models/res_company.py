# -*- encoding: utf-8 -*-
#
#Created on Jan 17, 2020
#
#@author: dogan
#
from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit='res.company'
    
    
    hash_code = fields.Char('Hash Comm Code', size=200, help="Used in comm with ext services")
        
