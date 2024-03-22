# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api


class CRMPhonecall(models.Model):
    _inherit = "crm.phonecall"

    activity_type_id = fields.Many2one(
        "mail.activity.type",
        string="Activity Type",
        required=True,
    )
    state = fields.Selection(
        selection_add=[("success", "Success"), ("failed", "Failed")]
    )
