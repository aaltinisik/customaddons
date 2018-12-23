# -*- encoding: utf-8 -*-
#
#Created on Dec 18, 2018
#
#@author: dogan
#

from openerp import models, api, fields


class stock_quant(models.Model):
    _inherit = 'stock.quant'

    ignore_reservation = fields.Boolean(related='location_id.ignore_reservation',store=True)
    priority = fields.Integer(related='location_id.priority', help='high priority quants will be reserved first',
                             readonly=True, store=True)

    @api.model
    def _quants_get_order(self, location, product, quantity, domain=[], orderby='in_date'):
        ''' overwrite default behavior
        '''
        
        if location and not location.ignore_reservation:
                domain += [('ignore_reservation','=',False)]
        return super(stock_quant, self)._quants_get_order(location=location, product=product, quantity=quantity,
                                                                  domain=domain, orderby=orderby)
    