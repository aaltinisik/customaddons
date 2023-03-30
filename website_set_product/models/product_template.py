# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    set_product = fields.Boolean(
        "Set product?",
        compute="_compute_set_product",
        help="Is this product a set product?"
        "If set, this product will not be shown in the shop.",
    )

    sub_component = fields.Boolean(
        "Sub component?",
        compute="_compute_sub_component",
        help="Is this product a sub-component of a set product?"
        "If set, this product will not be shown in the shop.",
    )

    def _compute_set_product(self):
        phantom_bom = (
            self.env["mrp.bom"]
            .sudo()
            .search([("product_tmpl_id", "=", self.id), ("type", "=", "phantom")])
        )
        if phantom_bom:
            self.set_product = True
        else:
            self.set_product = False

    def _compute_sub_component(self):
        """
        Multi record method to check if a product is a subcomponent of a set product.
        """
        query = f"""SELECT p.id, b.type
                FROM product_template p
                INNER JOIN (
                  SELECT DISTINCT bl.product_tmpl_id, b.type
                  FROM mrp_bom b
                  INNER JOIN mrp_bom_line bl ON b.id = bl.bom_id
                  WHERE b.type = 'phantom'
                ) AS b ON p.id = b.product_tmpl_id
                WHERE p.id IN {tuple(self.ids)}"""
        self.env.cr.execute(query)
        result = self.env.cr.fetchall()
        if result:
            result = set([x[0] for x in result])
            for product in self:
                product.sub_component = product.id in result
