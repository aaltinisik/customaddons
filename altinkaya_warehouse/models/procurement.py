# -*- encoding: utf-8 -*-
#
#Created on Jan 23, 2019
#
#@author: dogan
#
from openerp import models, api, fields


class ProcurementOrder(models.Model):
    _inherit = "procurement.order"

    @api.model
    def _prepare_orderpoint_procurement(self, orderpoint, product_qty):
        res = super(ProcurementOrder, self)._prepare_orderpoint_procurement(
            orderpoint, product_qty)
        if not orderpoint.group_id:
            group_id = self.env['procurement.group'].create({'name':'%s - %s' % (orderpoint.name, fields.Datetime.now() )})
            res['group_id'] = group_id.id
        return res