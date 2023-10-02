# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    description = fields.Html(
        string="Description",
        sanitize_attributes=False,
        compute="_compute_description",
    )
    description_page_id = fields.Many2one(
        comodel_name="website.page",
        string="Description Page",
        help="Page that contains the description of this category",
        # domain="[('website_id', '=', website_id)]",
    )

    def _compute_description(self):
        for category in self:
            if category.description_page_id:
                category.description = category.description_page_id.arch
            else:
                category.description = False
