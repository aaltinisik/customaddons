# -*- encoding: utf-8 -*-
#
#Created on Jan 20, 2020
#
#@author: dogan
#
from odoo import models, fields


class MigrationMapping(models.AbstractModel):
    _name = 'migration.mapping'
    
    old_id = fields.Id()

class ResPartner(models.Model):
    _inherit = ['res.partner', 'migration.mapping']
    
    
   
    
    