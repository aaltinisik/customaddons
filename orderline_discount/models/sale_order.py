# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    unit_discounted = fields.Float('Discounted Unit Price',
                                   compute='_compute_unit_discounted',
                                   digits_compute=dp.get_precision('Product Price'),
                                   readonly=True, states={'draft': [('readonly', False)]},
                                   store=False)

    @api.one
    @api.depends('price_unit', 'discount')
    def _compute_unit_discounted(self):
        self.unit_discounted = self.price_unit * ((100.0 -self.discount) / 100)

