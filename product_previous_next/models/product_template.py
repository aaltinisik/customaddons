# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    next_product = fields.Many2one(
        "product.template",
        string="Next Product",
        compute="_compute_next_product",
    )

    previous_product = fields.Many2one(
        "product.template",
        string="Previous Product",
        compute="_compute_previous_product",
    )

    """
    ZIn website_sale module "featured" sort is reversed. So don't worry about the
    computation with wrong domains.
    """

    def _compute_next_product(self):
        for record in self:
            next_product = self.env["product.template"].search(
                [
                    "&",
                    ("id", "!=", record.id),
                    ("id", "<", record.id),
                    ("is_published", "=", True),
                    ("categ_id", "=", record.categ_id.id),
                ],
                limit=1,
                order="website_sequence desc, id desc",
            )
            record.next_product = next_product

    def _compute_previous_product(self):
        for record in self:
            previous_product = self.env["product.template"].search(
                [
                    "&",
                    ("id", "!=", record.id),
                    ("id", ">", record.id),
                    ("is_published", "=", True),
                    ("categ_id", "=", record.categ_id.id),
                ],
                limit=1,
                order="website_sequence asc, id asc",
            )
            record.previous_product = previous_product
