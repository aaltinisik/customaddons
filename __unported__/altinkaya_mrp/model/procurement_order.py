# -*- encoding: utf-8 -*-
#
#Created on Oct 12, 2018
#
#@author: dogan
#
from openerp import models, fields, api

class procurement_order(models.Model):
    _inherit = 'procurement.order'
    
    @api.model
    def _prepare_mo_vals(self, procurement):
        res = super(procurement_order, self)._prepare_mo_vals(procurement)
        
        res.update({'priority':procurement.priority})
        
        return res
    