# -*- encoding: utf-8 -*-
#
#Created on Jan 20, 2020
#
#@author: dogan
#
from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    
    old_id = fields.Id()
    
    