# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields
from dateutil.relativedelta import relativedelta
from odoo.addons.base.models.ir_cron import _intervalTypes

# Monkey patching
_intervalTypes["seconds"] = lambda interval: relativedelta(seconds=interval)


class IrCron(models.Model):
    _inherit = "ir.cron"

    interval_type = fields.Selection(
        selection_add=[("seconds", "Seconds")],
        ondelete={"seconds": "set default"},
    )
