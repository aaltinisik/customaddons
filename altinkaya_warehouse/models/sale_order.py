# -*- encoding: utf-8 -*-
#
#Created on Apr 20, 2019
#
#@author: dogan
#

from openerp import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.multi
    def test_procurements_except(self):
        for sale in self:
            for line in sale.order_line:
                if line.state == 'cancel':
                    continue
                if any([x.state == 'cancel' for x in line.procurement_ids]):
                    return True
        return False