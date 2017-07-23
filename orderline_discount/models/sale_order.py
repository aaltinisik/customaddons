# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    unit_discounted = fields.Float('Disc. Unit',
                                   digits_compute=dp.get_precision('Product Price'),
                                   compute='_compute_unit_discounted',
                                   readonly=True, states={'draft': [('readonly', False)]},
                                   store=True)

    @api.one
    @api.depends('price_unit', 'discount')
    def _compute_unit_discounted(self):
        self.unit_discounted = round((self.price_unit * ((100.0 -self.discount) / 100.0)),4)


# from openerp import api, fields, models, _


# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'

#     discount_unit_price = fields.Float('Discount Unit Price')

#     @api.onchange('price_unit', 'discount')
#     def onchange_discount_price(self):
#         total_discount_price = 0.0
#         if self.discount:
#             total_discount_price = (self.price_unit * (100 - self.discount)) / 100
#         self.discount_unit_price = total_discount_price

#     @api.model
#     def create(self, vals):
#         price = vals.get('price_unit') or 0.0
#         discount = vals.get('discount') or 0.0
#         total_discount_price = (price * (100 - discount)) / 100
#         vals.update({'discount_unit_price': total_discount_price})
#         return super(SaleOrderLine, self).create(vals)

#     @api.multi
#     def write(self, vals):
#         print '>>>>>>>>>>>>>>>>>>>>>', vals
#         if not vals.get('discount_unit_price'):
#             price = vals.get('price_unit') or self.price_unit
#             discount = vals.get('discount') or self.discount
#             total_discount_price = (price * (100 - discount)) / 100
#             vals.update({'discount_unit_price': total_discount_price})
#         return super(SaleOrderLine, self).write(vals)
