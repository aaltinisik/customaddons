# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models
from odoo.http import request
from odoo.addons.altinkaya_seo.models.ir_http import slug


class IrQweb(models.AbstractModel):
    _inherit = "ir.qweb"

    def _prepare_environment(self, values):
        """
        Inherit slug method on Qweb environment.
        """
        irQweb = super()._prepare_environment(values)
        values["slug"] = slug

        if (
            not irQweb.env.context.get("minimal_qcontext")
            and request
            and request.is_frontend
        ):
            return irQweb._prepare_frontend_environment(values)

        return irQweb
