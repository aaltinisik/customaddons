# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    is_published = fields.Boolean(
        string="Published",
        help="If unchecked, it will allow you to hide the category without removing it.",
        related="origin_categ_id.is_published",
    )

    origin_categ_id = fields.Many2one(
        comodel_name="product.category",
        string="Origin Category",
        help="Origin category of this public category",
    )

    @api.model
    def _search_get_detail(self, website, order, options):
        """Add is_published field to search domain"""
        res = super(ProductPublicCategory, self)._search_get_detail(
            website, order, options
        )
        if res.get("base_domain", False):
            res["base_domain"].append([("is_published", "=", True)])

        return res

    def _compute_product_tmpls(self):
        """Link product templates for e-commerce"""
        tmpl_ids = self.env["product.template"].search(
            [
                ("categ_id", "=", self.origin_categ_id.id),
                ("is_published", "=", True),
            ]
        )
        if tmpl_ids:
            tmpl_ids.public_categ_ids = [(4, self.id)]
        return True
