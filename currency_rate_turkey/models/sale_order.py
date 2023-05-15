# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    @api.depends("currency_id", "date_order")
    def _compute_sale_currency_rate(self):
        currency_id = self.currency_id or self.env.user.company_id.currency_id
        if self.partner_id and self.partner_id.property_rate_field != "rate":
            curr_dict = currency_id.with_context(
                rate_type=self.partner_id.property_rate_field
            )._get_rates(self.env.user.company_id, self.date_order)
        else:
            curr_dict = currency_id._get_rates(
                self.env.user.company_id, self.date_order
            )
        self.sale_currency_rate = 1 / curr_dict.get(currency_id.id, 1.0)
        return True
