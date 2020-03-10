# -*- encoding: utf-8 -*-
#
#Created on Jan 20, 2020
#
#@author: dogan
#
from odoo import models,fields,api


class MigrationMapping(models.AbstractModel):
    _name = "migration.mapping"
    
    v8_id = fields.Integer(string="V8 ID",store=True)


# class ResPartner(models.Model):
#     _inherit = ['res.partner','migration.mapping']
#      
    
    
class Rescountry(models.Model):
    _name = 'res.country'
    _inherit= ["res.country",'migration.mapping'] 
    

    
