# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.multi
    def post(self):
        new_context = self._context.copy()
        if self.partner_id.property_rate_field != "rate":
            new_context.update(
                {
                    "rate_type": self.partner_id.property_rate_field,
                }
            )
        return super(AccountPayment, self.with_context(new_context)).post()
