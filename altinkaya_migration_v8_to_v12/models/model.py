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
    
class RescountryState(models.Model):
    _name = 'res.country.state'
    _inherit= ["res.country.state",'migration.mapping']

class AddressDistrict(models.Model):
    _name = 'address.district'
    _inherit= ["address.district",'migration.mapping']

class AddressRegion(models.Model):
    _name = 'address.region'
    _inherit= ["address.region",'migration.mapping']

class AddressNeighbour(models.Model):
    _name = 'address.neighbour'
    _inherit= ["address.neighbour",'migration.mapping']



