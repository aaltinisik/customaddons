# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models
from odoo.http import request


class HttpInherit(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _get_error_html(cls, env, code, values):
        if code == 404:
            website = request.website
            if website and website.catch_404_errors:
                website._catch_404_error(request.httprequest)
        return super()._get_error_html(env, code, values)
