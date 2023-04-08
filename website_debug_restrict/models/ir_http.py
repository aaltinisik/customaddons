# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models
from odoo.http import request


class HttpInherit(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _handle_debug(cls):
        """
        Check if the user is in the debug group and if not, disable debug mode
        """
        super(HttpInherit, cls)._handle_debug()
        if request.env.user and not request.env.user.has_group(
            "website_debug_restrict.restrict_debug_mode"
        ):
            request.session.debug = ""
