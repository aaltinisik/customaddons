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
    In website_sale module "featured" sort is reversed. So don't worry about the
    computation with wrong domains.
    """

    def _base_order_domain(self, website_id):
        return [
            ("id", "!=", self.id),
            ("sale_ok", "=", True),
            ("categ_id.is_published", "=", True),
            ("is_published", "=", True),
            ("sub_component", "=", False),
            ("public_categ_ids", "=", self.mapped("public_categ_ids.id")),
            ("website_id", "in", [website_id.id, False]),
        ]

    def _compute_next_product(self):
        website_id = self.env["website"].get_current_website()
        for record in self:
            base_dom = record._base_order_domain(website_id)
            next_product = self.env["product.template"].search(
                [
                    "|",
                    ("website_sequence", "=", record.website_sequence),
                    ("website_sequence", ">", record.website_sequence),
                    ("id", ">", record.id),
                ]
                + base_dom,
                limit=1,
                order="is_published desc, website_sequence asc, id desc",
            )
            record.next_product = next_product

    def _compute_previous_product(self):
        website_id = self.env["website"].get_current_website()
        for record in self:
            base_dom = record._base_order_domain(website_id)
            previous_product = self.env["product.template"].search(
                [
                    "|",
                    ("website_sequence", "=", record.website_sequence),
                    ("website_sequence", "<", record.website_sequence),
                    ("id", "<", record.id),
                ]
                + base_dom,
                limit=1,
                order="is_published desc, website_sequence asc, id desc",
            )
            record.previous_product = previous_product
