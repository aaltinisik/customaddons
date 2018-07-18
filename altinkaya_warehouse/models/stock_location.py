# -*- encoding: utf-8 -*-
#
#Created on Jul 2, 2018
#
#@author: dogan
#
from openerp import models, fields, api


class stock_location(models.Model):
    _inherit = 'stock.location'
    
    @api.multi
    def button_barcode_generate(self):
        self.ensure_one()
        if not self.loc_barcode:
            self.loc_barcode = self.env['ir.sequence'].next_by_code('location.barcode')
            
