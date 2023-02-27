# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, api


class Website(models.Model):
    _inherit = "website"

    @api.model
    def pager(self, url, total, page=1, step=30, scope=5, url_args=None):
        """Overwrite this method to use custom paths."""
        if "/shop/category" in url:
            categ_slug = url.split("/shop/category/")[-1]
            new_slug = "-".join(categ_slug.split("-")[:-1])
            url = "/urunler/%s" % new_slug

        if "/shop" in url:
            url = "/urunler"

        return super(Website, self).pager(
            url, total, page=page, step=step, scope=scope, url_args=url_args
        )
