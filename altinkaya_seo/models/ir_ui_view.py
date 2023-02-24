# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    """
    We need to translate the name field of the ir.ui.view model to fix page title.
    TODO yigit: maybe there is a better way to do this.
    """
    name = fields.Char(translate=False)
    name_tr = fields.Char("Turkish Name")
