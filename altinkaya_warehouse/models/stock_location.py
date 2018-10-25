# -*- encoding: utf-8 -*-
#
#Created on Jul 2, 2018
#
#@author: dogan
#
from openerp import models, fields, api
from openerp import exceptions


class stock_location(models.Model):
    _inherit = 'stock.location'
    _order = 'loc_barcode'
    
    @api.multi
    def button_barcode_generate(self):
        self.ensure_one()
        if not self.loc_barcode:
            self.loc_barcode = self._generate_ean13_value()
            



    def _get_ean_control_digit(self, code):
        def isodd(x):
            return bool(x % 2)
        
        sum = 0
        for i in range(12):
            if isodd(i):
                sum += 3 * int(code[i])
            else:
                sum += int(code[i])
        key = (10 - sum % 10) % 10
        return '%d' % key

    def _generate_ean13_value(self):
        ean = self.env['ir.sequence'].next_by_code('location.barcode')
        ean = (len(ean[0:6]) == 6 and ean[0:6] or
               ean[0:6].ljust(6, '0')) + ean[6:].rjust(6, '0')
        if len(ean) > 12:
            raise exceptions.Warning(
                _("Configuration Error!"
                  "The next sequence is longer than 12 characters. "
                  "It is not valid for an EAN13 needing 12 characters, "
                  "the 13 being used as a control digit"
                  "You will have to redefine the sequence or create a new one")
                )

        if not ean:
            return None
        key = self._get_ean_control_digit(ean)
        ean13 = ean + key
        return ean13
    
    @api.model
    def create(self, vals):
        if not vals.get('loc_barcode'):
            vals['loc_barcode'] = self._generate_ean13_value()
        return super(stock_location, self).create(vals)
        

