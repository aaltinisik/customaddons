# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_move_create(self):
        new_context = self._context.copy()
        if self.partner_id.property_rate_type != "rate" and not self.use_custom_rate:
            new_context.update(
                {
                    "rate_type": self.partner_id.property_rate_type,
                }
            )
        return super(
            AccountInvoice, self.with_context(new_context)
        ).action_move_create()
