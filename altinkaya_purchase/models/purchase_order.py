# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    pricelist_id = fields.Many2one('product.pricelist',
                                   'Pricelist',
                                   required=True,
                                   default=lambda self: self.partner_id.property_product_pricelist,
                                   states={'draft': [('readonly', False)],
                                           'sent': [('readonly', True)]},
                                   help="Pricelist for current purchase order.")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for order in self:
            if order.partner_id and order.partner_id.property_product_pricelist:
                order.pricelist_id = order.partner_id.property_product_pricelist

    @api.multi
    def recalculate_prices(self):
        for line in self.mapped('order_line'):
            dict = line._convert_to_write(line.read()[0])
            line2 = self.env['purchase.order.line'].new(dict)
            # we make this to isolate changed values:
            line2.product_uom_change()
            line.write({
                'price_unit': line2.price_unit,
            })
        return True


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        res = super(PurchaseOrderLine, self)._onchange_quantity()
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            self.price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product),
                                                                                      product.taxes_id, self.taxes_id,
                                                                                      self.company_id)
        return res

    @api.multi
    def _get_display_price(self, product):
        if self.order_id.pricelist_id.discount_policy == 'with_discount':
            return product.with_context(pricelist=self.order_id.pricelist_id.id, uom=self.product_uom.id).price
        product_context = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order,
                               uom=self.product_uom.id)
        supplier_info = product.seller_ids.filtered(lambda r: r.name == self.order_id.partner_id)
        final_price, rule_id = self.order_id.pricelist_id.with_context(product_context).get_product_price_rule(
            product or self.product_id, self.product_qty or 1.0, self.order_id.partner_id)
        # base_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id,
        #                                                                                    self.product_qty,
        #                                                                                    self.product_uom,
        #                                                                                    self.order_id.pricelist_id.id)
        price_currency = supplier_info.currency_id
        if price_currency != self.order_id.pricelist_id.currency_id:
            final_price = price_currency._convert(
                price_currency, self.order_id.pricelist_id.currency_id,
                self.order_id.company_id or self.env.user.company_id, self.order_id.date_order or fields.Date.today())
        # negative discounts (= surcharge) are included in the display price
        return final_price

    def _get_real_price_currency(self, product, rule_id, qty, uom, pricelist_id):
        """Retrieve the price before applying the pricelist
            :param obj product: object of current product record
            :parem float qty: total quentity of product
            :param tuple price_and_rule: tuple(price, suitable_rule) coming from pricelist computation
            :param obj uom: unit of measure of current order line
            :param integer pricelist_id: pricelist id of purchase order"""
        return 0.0
        # PricelistItem = self.env['product.pricelist.item']
        # field_name = 'attr_price'
        # currency_id = None
        # product_currency = product.currency_id
        # if rule_id:
        #     pricelist_item = PricelistItem.browse(rule_id)
        #     if pricelist_item.pricelist_id.discount_policy == 'without_discount':
        #         while pricelist_item.base == 'pricelist' and pricelist_item.base_pricelist_id and pricelist_item.base_pricelist_id.discount_policy == 'without_discount':
        #             price, rule_id = pricelist_item.base_pricelist_id.with_context(uom=uom.id).get_product_price_rule(
        #                 product, qty, self.order_id.partner_id)
        #             pricelist_item = PricelistItem.browse(rule_id)
        #
        #     if pricelist_item.base == 'standard_price':
        #         field_name = 'standard_price'
        #         product_currency = product.cost_currency_id
        #     elif pricelist_item.base == 'pricelist' and pricelist_item.base_pricelist_id:
        #         field_name = 'price'
        #         product = product.with_context(pricelist=pricelist_item.base_pricelist_id.id)
        #         product_currency = pricelist_item.base_pricelist_id.currency_id
        #     currency_id = pricelist_item.pricelist_id.currency_id
        #
        # if not currency_id:
        #     currency_id = product_currency
        #     cur_factor = 1.0
        # else:
        #     if currency_id.id == product_currency.id:
        #         cur_factor = 1.0
        #     else:
        #         cur_factor = currency_id._get_conversion_rate(product_currency, currency_id,
        #                                                       self.company_id or self.env.user.company_id,
        #                                                       self.order_id.date_order or fields.Date.today())
        #
        # product_uom = self.env.context.get('uom') or product.uom_id.id
        # if uom and uom.id != product_uom:
        #     # the unit price is in a different uom
        #     uom_factor = uom._compute_price(1.0, product.uom_id)
        # else:
        #     uom_factor = 1.0
        #
        # return product[field_name] * uom_factor * cur_factor, currency_id
