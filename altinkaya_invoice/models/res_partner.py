# -*- encoding: utf-8 -*-
#
#Created on Jan 17, 2020
#
#@author: dogan
#
from odoo import models, fields, api

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    #altinkaya61
    z_muhasebe_kodu = fields.Char('Zirve Muhasebe kodu', size=64, required=False, translate=False)
    