# -*- encoding: utf-8 -*-
#
#Created on Jan 17, 2020
#
#@author: dogan
#
from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'
    
    default_procurement_wh_id = fields.Many2one('stock.warehouse',string='Default Procurement Warehouse')


