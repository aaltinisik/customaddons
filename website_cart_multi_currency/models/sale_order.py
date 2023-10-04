# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    company_currency_id = fields.Many2one(
        related="company_id.currency_id",
        readonly=True,
    )

    amount_total_company_currency = fields.Monetary(
        compute="_compute_amount_total_currency",
        string="Total",
        # store=True,
        currency_field="company_currency_id",
    )

    currency_rate = fields.Float(
        compute="_compute_currency_rate",
        digits=(12, 4),
    )

    inverse_currency_rate = fields.Float(
        compute="_compute_currency_rate",
        digits=(12, 4),
    )

    def _compute_amount_total_currency(self):
        for order in self:
            order.amount_total_company_currency = order.currency_id._convert(
                order.amount_total,
                order.company_currency_id,
                order.company_id,
                order.date_order,
            )

    @api.depends("currency_id", "company_id.currency_id")
    def _compute_currency_rate(self):
        for order in self:
            if order.currency_id != order.company_id.currency_id:
                order.currency_rate = order.currency_id._convert(
                    1.0,
                    order.company_id.currency_id,
                    order.company_id,
                    order.date_order,
                    round=False,
                )
                order.inverse_currency_rate = order.company_id.currency_id._convert(
                    1.0,
                    order.currency_id,
                    order.company_id,
                    order.date_order,
                    round=False,
                )
            else:
                order.currency_rate = 1.0
                order.inverse_currency_rate = 1.0
