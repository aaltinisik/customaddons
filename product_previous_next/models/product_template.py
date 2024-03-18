# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    next_product = fields.Many2one(
        "product.template",
        string="Next Product",
        compute="_compute_next_previous_product",
    )

    previous_product = fields.Many2one(
        "product.template",
        string="Previous Product",
        compute="_compute_next_previous_product",
    )

    def _base_order_domain(self, website_id):
        return [
            ("sale_ok", "=", True),
            ("categ_id.is_published", "=", True),
            ("is_published", "=", True),
            ("public_categ_ids", "in", self.mapped("public_categ_ids.id")),
            ("website_id", "in", [website_id.id, False]),
        ]

    def _compute_next_previous_product(self):
        self.ensure_one()
        website_id = self.env["website"].get_current_website()
        domain = self._base_order_domain(website_id)

        ordered_ids = list(
            reversed(
                self.env["product.template"]
                .search(
                    domain,
                    order="is_published desc, website_sequence asc, name asc, id desc",
                )
                .ids
            )
        )

        # Find the previous and next product ids in the ordered list
        try:
            current_index = ordered_ids.index(self.id)
        except ValueError:
            self.previous_product = False
            self.next_product = False
            return True
        previous_index = current_index - 1
        next_index = current_index + 1
        self.previous_product = (
            ordered_ids[previous_index] if previous_index >= 0 else False
        )
        self.next_product = (
            ordered_ids[next_index] if next_index < len(ordered_ids) else False
        )
        return True
