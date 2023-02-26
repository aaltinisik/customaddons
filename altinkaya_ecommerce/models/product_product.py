# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields, models
from collections import OrderedDict


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Override the field to remove the domain
    product_template_variant_value_ids = fields.Many2many(domain=[])
    v_cari_urun = fields.Many2one("res.partner", string="Partner Special Product")

    def price_compute(
        self, price_type, uom=None, currency=None, company=None, date=False
    ):
        """Override price_compute method to use sale_price field."""
        res = super(ProductProduct, self).price_compute(
            "sale_price", uom=uom, currency=currency, company=company, date=date
        )
        return res

    def _prepare_categories_for_display(self):
        """
        This method adds features along with attributes to the comparison table.
        """
        res = super(ProductProduct, self)._prepare_categories_for_display()
        features = self.product_tmpl_id.feature_line_ids.attribute_id.sorted()
        for pa in features:
            res[pa.category_id][pa] = OrderedDict(
                [
                    (
                        product,
                        product.product_tmpl_id.feature_line_ids.value_ids.filtered(
                            lambda ptav: ptav.attribute_id == pa
                        ),
                    )
                    for product in self
                ]
            )
        return res
