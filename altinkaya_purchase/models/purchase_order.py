# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    pricelist_id = fields.Many2one(
        "product.pricelist",
        "Pricelist",
        required=True,
        default=lambda self: self.partner_id.property_product_pricelist,
        states={"draft": [("readonly", False)], "sent": [("readonly", True)]},
        help="Pricelist for current purchase order.",
    )

    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)
        if res.partner_id and res.partner_id.property_purchase_pricelist:
            res.pricelist_id = res.partner_id.property_purchase_pricelist
        return res

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        for order in self:
            if order.partner_id and order.partner_id.property_purchase_pricelist:
                order.pricelist_id = order.partner_id.property_purchase_pricelist

    @api.multi
    def recalculate_prices(self):
        for line in self.mapped("order_line"):
            dict = line._convert_to_write(line.read()[0])
            line2 = self.env["purchase.order.line"].new(dict)
            # we make this to isolate changed values:
            line2.onchange_product_id()
            line.write(
                {
                    "taxes_id": line2.taxes_id,
                    "name": line2.name,
                    "price_unit": line2.price_unit,
                }
            )
        return True


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.onchange("product_qty", "product_uom")
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
                fiscal_position=self.env.context.get("fiscal_position"),
            )
            self.price_unit = self.env["account.tax"]._fix_tax_included_price_company(
                self._get_display_price(product),
                product.taxes_id,
                self.taxes_id,
                self.company_id,
            )
        return res

    @api.multi
    def _get_display_price(self, product):
        supplier_info = product.seller_ids.filtered(
            lambda r: r.name == self.order_id.partner_id
        )
        if self.order_id.pricelist_id.discount_policy == "with_discount":
            return product.with_context(
                pricelist=self.order_id.pricelist_id.id, uom=self.product_uom.id
            ).price
        product_context = dict(
            self.env.context,
            partner_id=self.order_id.partner_id,
            date=self.order_id.date_order,
            uom=self.product_uom.id,
        )
        final_price, rule_id = self.order_id.pricelist_id.with_context(
            product_context
        ).get_product_price_rule(
            product or self.product_id,
            self.product_qty or 1.0,
            self.order_id.partner_id,
        )
        price_currency = supplier_info.currency_id
        if price_currency != self.order_id.pricelist_id.currency_id:
            final_price = price_currency._convert(
                final_price,
                self.order_id.pricelist_id.currency_id,
                self.order_id.company_id or self.env.user.company_id,
                self.order_id.date_order or fields.Date.today(),
            )
        # negative discounts (= surcharge) are included in the display price
        return final_price
