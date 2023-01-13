# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, api


class AccountAccount(models.Model):
    _inherit = "account.account"

    @api.constrains("code")
    def _check_account_code(self):
        """Override
        account.account record name can have Turkish characters.
        we don't need this control.
        """
        return True
