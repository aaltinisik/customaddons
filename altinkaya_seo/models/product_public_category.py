# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api
from odoo.addons.altinkaya_seo.models.ir_http import slug


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    seo_name = fields.Char(
        string="SEO Name",
        help="SEO Name for product",
        compute="_compute_seo_name",
        store=True,
    )

    @api.depends("name")
    def _compute_seo_name(self):
        for category in self:
            # we need to set it to empty string first
            category.seo_name = ""
            category.seo_name = slug(category)

    def _search_render_results(self, fetch_fields, mapping, icon, limit):
        results_data = super()._search_render_results(
            fetch_fields, mapping, icon, limit
        )
        for data in results_data:
            category = self.browse(data["id"])
            data["url"] = "/urunler/%s" % category.seo_name
        return results_data
