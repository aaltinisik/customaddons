# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    kdv_amount = fields.Monetary(
        default=0.0,
        currency_field="company_currency_id",
        string="Amount Total Currency",
        compute="_compute_kdv_amount",
        store=True,
        help="Total amount in company currency."
        " We use this field in account reporting.",
    )

    @api.depends(
        "invoice_id.date_invoice",
        "invoice_id.currency_id",
        "invoice_id.custom_rate",
        "invoice_line_tax_ids",
        "price_subtotal",
    )
    def _compute_kdv_amount(self):
        for ail in self:
            currency_rate = ail.invoice_id.custom_rate
            kdv_amount = 0.0
            for tax in ail.invoice_line_tax_ids:
                if tax.account_id.code.startswith("191.0"):
                    kdv_amount -= ail.price_subtotal * tax.amount / 100
                elif tax.account_id.code.startswith("391.0"):
                    kdv_amount += ail.price_subtotal * tax.amount / 100
            # Convert to company currency
            if ail.currency_id != ail.company_currency_id and currency_rate > 0.00001:
                kdv_amount = kdv_amount / currency_rate

            ail.kdv_amount = kdv_amount

"""

UPDATE
          account_invoice_line AS ail
        SET
          kdv_amount = subquery.total_kdv
        FROM
          (
            SELECT
              ail.id AS line_id,
              SUM(
                CASE WHEN aa.code LIKE '191.0%' THEN -1 * (
                  ail.price_subtotal * at.amount / 100
                ) WHEN aa.code LIKE '391.0%' THEN ail.price_subtotal * at.amount / 100 ELSE 0 END
              ) * CASE WHEN rc.id != 31
              and ai.custom_rate > 0.00001 THEN 1 / ai.custom_rate ELSE 1 END AS total_kdv
            FROM
              account_invoice_line AS ail
              LEFT JOIN account_invoice_line_tax AS ailt ON ail.id = ailt.invoice_line_id
              LEFT JOIN account_tax AS at ON at.id = ailt.tax_id
              LEFT JOIN account_account AS aa ON at.account_id = aa.id
              LEFT JOIN account_invoice AS ai ON ail.invoice_id = ai.id
              LEFT JOIN res_currency AS rc ON ai.currency_id = rc.id
              LEFT JOIN res_currency_rate AS rcr ON rcr.currency_id = rc.id
              AND rcr.name = ai.date_invoice
            WHERE
              aa.code LIKE '191.0%'
              OR aa.code LIKE '391.0%'
            GROUP BY
              ail.id,
              rc.id,
              ai.custom_rate
          ) AS subquery
        WHERE
          ail.id = subquery.line_id;


"""
