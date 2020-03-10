# -*- encoding: utf-8 -*-
#
#Created on Jan 20, 2020
#
#@author: dogan
#
from odoo import models,fields,api


class MigrationMapping(models.AbstractModel):
    _name = "migration.mapping"
    
    v8_id = fields.Integer(string="V8 ID")


class ResPartner(models.Model):
    _inherit = ['res.partner','migration.mapping']
    
    
    
class ResCountry(models.Model):
    _inherit= ["res.country",'migration.mapping'] 
    

    
