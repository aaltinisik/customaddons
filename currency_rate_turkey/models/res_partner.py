# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_rate_field = fields.Selection(
        selection=lambda self: self.env["res.currency.rate"]._get_rate_fields(),
        default="rate",
        required=True,
        string="Currency Rate Field",
    )
