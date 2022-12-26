# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    tax_office_name = fields.Char(
        string="Tax Office Name",
        help="Tax Office Name",
        copy=False,
    )
