# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('price_unit', 'discount')
    # @api.onchange('product_uom_qty', 'price_unit', 'discount')
    def onchange_discount_price(self):
        total_discount_price = 0.0
        if self.discount:
#            total_discount_price = (self.product_uom_qty * self.price_unit * self.discount) / 100
            total_discount_price = (self.price_unit * (100 - self.discount)) / 100
        self.discount_unit_price = total_discount_price

    discount_unit_price = fields.Float('Discount Unit Price')

    @api.model
    def create(self, vals):
        # qty = vals.get('product_uom_qty') or 0.0
        price = vals.get('price_unit') or 0.0
        discount = vals.get('discount') or 0.0
#        total_discount_price = (qty * price * discount) / 100
        total_discount_price = (price * (100 - discount)) / 100
        vals.update({'discount_unit_price': total_discount_price})
        return super(SaleOrderLine, self).create(vals)

    @api.multi
    def write(self, vals):
        # qty = vals.get('product_uom_qty') or self.product_uom_qty
        price = vals.get('price_unit') or self.price_unit
        discount = vals.get('discount') or self.discount
#        total_discount_price = (qty * price * discount) / 100
        total_discount_price = (price * (100 - discount)) / 100
        vals.update({'discount_unit_price': total_discount_price})
        return super(SaleOrderLine, self).write(vals)
