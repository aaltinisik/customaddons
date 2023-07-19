"""
Created on Jan 17, 2019

@author: cq
"""
from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


# Aktarıldı
class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"
    attr_base_price = fields.Float(
        "Base Price",
        digits=dp.get_precision("Product Price"),
        help="Base price used to compute product price based on attribute value.",
    )
    attr_val_price_coef = fields.Float(
        "Value Price Multiplier",
        digits=dp.get_precision("Product Price"),
        help="Attribute value coefficient used to compute product price based on attribute value.",
    )
    use_in_pricing = fields.Boolean("Use in pricing")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # for sale configurator
    attr_price = fields.Float(
        digits=dp.get_precision("Product Price"),
        string="Attr. Value Price",
        help="Price calculated based on the product's attribute values.",
        default=0.0,
    )
    v_tl_fiyat = fields.Float(
        "USD Fiyatı",
        digits=dp.get_precision("Product Price"),
        help="Birim işçilik Fiyatı USD",
        default=0.0,
    )
    v_iscilik_fiyat = fields.Float(
        "işçilik Fiyatı USD",
        digits=dp.get_precision("Product Price"),
        help="Birim işçilik Fiyatı USD",
        default=0.0,
    )
    v_min_iscilik_fiy = fields.Float(
        "Minimum işçilik Fiyatı USD",
        digits=dp.get_precision("Product Price"),
        help="En Az Toplam işçilik Fiyatı USD",
        default=0.0,
    )
    v_guncel_fiyat = fields.Boolean(
        "Fiyat Güncel", help="Bu seçenek seçili ise fiyatı yenidir.", default=0.0
    )

    # altinkaya
    v_fiyat_dolar = fields.Float(
        "Dolar Fiyatı",
        digits=dp.get_precision("Product Price"),
        help="Dolarla satılan ürünlerin fiyatı",
        default=0.0,
    )
    v_fiyat_euro = fields.Float(
        "Euro Fiyatı",
        digits=dp.get_precision("Product Price"),
        help="Euro ile satılırken kullanılan temel fiyat",
        default=0.0,
    )

    has_production_bom = fields.Boolean(
        "Has production BoM", compute="_compute_has_production_bom", store=True
    )

    @api.one
    @api.depends("bom_ids", "bom_ids.type")
    def _compute_has_production_bom(self):
        self.has_production_bom = any(
            self.bom_ids.filtered(lambda b: b.type != "phantom")
        )

    def compute_set_product_price(self):
        """
        Compute the price of the set product based on the price of its components.
        It creates a dummy SO to compute the price of the components.
        :return:
        """
        self.ensure_one()
        phantom_boms = self.bom_ids.filtered(lambda b: b.type == "phantom")

        if not phantom_boms:
            raise UserError(
                _(
                    "No phantom BoM found for product %s. Please create"
                    " a phantom BoM to compute the price of the set product."
                    % self.name
                )
            )

        products_2compute = self.product_variant_ids
        date_now = fields.Datetime.now()
        dummy_so = self.env["sale.order"].create(
            {
                "name": "Phantom Bom Price Compute: %s, %s"
                % (self.id, date_now.strftime("%d-%m-%Y")),
                "partner_id": 12515,  # Ahmet Altınışık test
                "partner_invoice_id": 12515,
                "partner_shipping_id": 12515,
                "pricelist_id": 136,  # USD pricelist
                "warehouse_id": 1,
                "company_id": 1,
                "currency_id": 2,  # USD
                "date_order": fields.Datetime.now(),
            }
        )
        for product in products_2compute:
            # Create a new sale order line
            dummy_sol = self.env["sale.order.line"].create(
                {
                    "order_id": dummy_so.id,
                    "product_id": product.id,
                    "product_uom_qty": 1,
                    "product_uom": product.uom_id.id,
                }
            )
            # Explode the phantom bom
            dummy_sol.explode_set_contents()
            # Compute the price
            dummy_so.recalculate_prices()
            # Update the product price
            _logger.info(
                "Updating product price for product %s: %s -> %s"
                % (product.name, product.v_fiyat_dolar, dummy_so.amount_untaxed)
            )
            product.v_fiyat_dolar = dummy_so.amount_untaxed
            # Clear sale order lines
            dummy_so.order_line.unlink()
        # Clear the dummy sale order
        dummy_so.unlink()
        self.env.cr.commit()
        return True
