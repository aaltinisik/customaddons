# -*- encoding: utf-8 -*-
#
#Created on Dec 18, 2018
#
#@author: dogan
#

from openerp import models, api, fields


class stock_quant(models.Model):
    _inherit = 'stock.quant'
    
    
    @api.model
    def _quants_get_order(self, location, product, quantity, domain=[], orderby='in_date'):
        ''' overwrite default behavior
        '''
        
        child_locations = self.env['stock.location'].search([('id','child_of',location.id),('ignore_reservation','=',False)])
        
        domain += location and [('location_id', 'in', child_locations.ids)] or []
        
        return super(stock_quant, self)._quants_get_order(location=None,product=product, domain=domain, order_by=orderby)
        
        
        
        
        
        