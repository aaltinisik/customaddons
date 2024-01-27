# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api, _


class ResPartnerSegment(models.Model):
    _name = "res.partner.segment"
    _description = "Partner Segment"

    active = fields.Boolean(default=True)
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    description = fields.Text(string="Description")
    partner_ids = fields.One2many(
        comodel_name="res.partner",
        inverse_name="segment_id",
        string="Partners",
        ondelete="cascade",
    )
