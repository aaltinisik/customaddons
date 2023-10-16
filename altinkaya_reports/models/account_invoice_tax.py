# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api


class AccountInvoiceTax(models.Model):
    _inherit = "account.invoice.tax"

    company_currency_id = fields.Many2one(
        related="invoice_id.company_id.currency_id",
        string="Company Currency",
        readonly=True,
        store=True,
    )

    amount_total_currency = fields.Monetary(
        default=0.0,
        currency_field="company_currency_id",
        string="Amount Total Currency",
        compute="_compute_amount_total_currency",
        store=True,
        help="Total amount in company currency."
        " We use this field in account reporting.",
    )

    @api.depends("amount_total", "currency_id")
    def _compute_amount_total_currency(self):
        """
        Compute amount_total_currency field for account reporting.
        :return:
        """
        query = """
            UPDATE account_invoice_tax ait
            SET amount_total_currency = CASE 
                    WHEN ait.currency_id != ai.company_currency_id
                        AND ai.custom_rate > 0.001
                        THEN ait.amount / ai.custom_rate
                    ELSE ait.amount
                    END
            FROM account_invoice ai
            WHERE ait.invoice_id = ai.id
                AND ait.id IN %s;
        """
        self.env.cr.execute(query, [tuple(self.ids)])
        self.env.cr.commit()
