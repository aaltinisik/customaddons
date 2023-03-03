# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models, tools
from itertools import chain
from odoo.exceptions import UserError


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _compute_price_rule(self, products, qty, uom=None, date=False, **kwargs):
        """Low-level method - Mono pricelist, multi products
        Returns: dict{product_id: (price, suitable_rule) for the given pricelist}

        :param products: recordset of products (product.product/product.template)
        :param float qty: quantity of products requested (in given uom)
        :param uom: unit of measure (uom.uom record)
            If not specified, prices returned are expressed in product uoms
        :param date: date to use for price computation and currency conversions
        :type date: date or datetime

        :returns: product_id: (price, pricelist_rule)
        :rtype: dict
        """
        self.ensure_one()
        if not products:
            return {}
        if not date:
            # Used to fetch pricelist rules and currency rates
            date = fields.Datetime.now()
        # Fetch all rules potentially matching specified products/templates/categories and date
        rules = self._get_applicable_rules(products, date, **kwargs)
        results = {}
        for product in products:
            suitable_rule = self.env["product.pricelist.item"]

            product_uom = product.uom_id
            target_uom = (
                uom or product_uom
            )  # If no uom is specified, fall back on the product uom

            # Compute quantity in product uom because pricelist rules are specified
            # w.r.t product default UoM (min_quantity, price_surchage, ...)
            if target_uom != product_uom:
                qty_in_product_uom = target_uom._compute_quantity(
                    qty, product_uom, raise_if_failure=False
                )
            else:
                qty_in_product_uom = qty

            for rule in rules:
                if rule._is_applicable_for(product, qty_in_product_uom):
                    suitable_rule = rule
                    break

            kwargs["pricelist"] = self
            price = suitable_rule._compute_price(
                product, qty, target_uom, date=date, currency=self.currency_id
            )
            results[product.id] = (price, suitable_rule.id)

        return results


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    base = fields.Selection(
        selection_add=[("sale_price", "Website Sale Price")],
        ondelete={"sale_price": "set default"},
    )

    # def _compute_base_price(self, product, quantity, uom, date, target_currency):
    #     """Compute the base price for a given rule
    #
    #     :param product: recordset of product (product.product/product.template)
    #     :param float qty: quantity of products requested (in given uom)
    #     :param uom: unit of measure (uom.uom record)
    #     :param datetime date: date to use for price computation and currency conversions
    #     :param target_currency: pricelist currency
    #
    #     :returns: base price, expressed in provided pricelist currency
    #     :rtype: float
    #     """
    #     target_currency.ensure_one()
    #     usd_currency = self.env.ref("base.USD")
    #     rule_base = self.base or "list_price"
    #     if rule_base == "pricelist" and self.base_pricelist_id:
    #         price = self.base_pricelist_id._get_product_price(
    #             product, quantity, uom, date
    #         )
    #         src_currency = self.base_pricelist_id.currency_id
    #     elif rule_base == "standard_price":
    #         src_currency = product.cost_currency_id
    #         price = product.price_compute(rule_base, uom=uom, date=date)[product.id]
    #
    #     elif rule_base == "sale_price":
    #         src_currency = usd_currency
    #         price = product.price_compute(rule_base, uom=uom, date=date)[product.id]
    #
    #     else:  # list_price
    #         src_currency = product.currency_id
    #         price = product.price_compute(rule_base, uom=uom, date=date)[product.id]
    #
    #     if src_currency != target_currency:
    #         price = src_currency._convert(
    #             price, target_currency, self.env.company, date, round=False
    #         )
    #
    #     return price
