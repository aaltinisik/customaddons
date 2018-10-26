# -*- encoding: utf-8 -*-
#
#Created on Oct 26, 2018
#
#@author: dogan
#

from openerp import models, fields


class ResUser(models.Model):
    _inherit = 'res.users'
    
    default_procurement_wh_id = fields.Many2one('stock.warehouse',string='Default Procurement Warehouse')
