# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class MRPBoM(models.Model):
    _inherit = "mrp.bom"

    bom_template_line_ids = fields.One2many(
        "mrp.bom.template.line", "bom_id", "BoM Template Lines"
    )
