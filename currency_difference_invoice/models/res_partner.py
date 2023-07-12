# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.one
    def _compute_currency_difference_amls(self):
        difference_aml_domain = [
            ("partner_id", "=", self.id),
            ("journal_id", "=", self.company_id.currency_exchange_journal_id.id),
            ("difference_checked", "=", False),
            ("full_reconcile_id", "!=", False),
        ]

        difference_amls = self.env["account.move.line"].search(difference_aml_domain)
        if len(difference_amls) > 0:
            self.currency_difference_amls = difference_amls
        else:
            self.currency_difference_amls = False

    @api.multi
    @api.depends("currency_difference_amls")
    def _compute_difference_to_invoice(self):
        for partner in self:
            if len(partner.currency_difference_amls) > 0:
                partner.difference_to_invoice = True
            else:
                partner.difference_to_invoice = False

    @api.multi
    def _value_search_diff_check(self, operator, value):
        AccountMoveLine = self.env["account.move.line"]
        domain = [
            ("difference_checked", "=", False),
            (
                "journal_id",
                "=",
                self.env.user.company_id.currency_exchange_journal_id.id,
            ),
        ]

        result = [
            res["partner_id"][0]
            for res in AccountMoveLine.read_group(
                domain, ["partner_id"], ["partner_id"]
            )
        ]
        return [("id", "in", result)]

    currency_difference_amls = fields.Many2many(
        "account.move.line",
        string="Currency Difference Move Lines",
        compute="_compute_currency_difference_amls",
    )

    currency_difference_to_invoice = fields.Boolean(
        string="Currency Difference to invoice",
        compute="_compute_difference_to_invoice",
        default=False,
        store=False,
        search="_value_search_diff_check",
    )

    currency_difference_checked = fields.Boolean(
        string="Currency Difference Checked",
        default=False,
        help="Manual check for currency difference",
    )

    def unreconcile_partners_amls(self):
        if (
            self.property_account_receivable_id.currency_id
            and self.property_account_payable_id.currency_id
        ):
            reconciled_amls = self.env["account.move.line"].search(
                [("partner_id", "=", self.id), ("full_reconcile_id", "!=", False)]
            )
            if reconciled_amls:
                reconciled_amls.remove_move_reconcile()

    def calc_difference_invoice(self, date, payment_term, billing_point):
        if (
            self.property_account_receivable_id.currency_id
            and self.property_account_payable_id.currency_id
        ):
            inv_obj = self.env["account.invoice"]
            diff_inv_journal = self.env["account.journal"].search(
                [("code", "=", "KFARK")], limit=1
            )
            draft_dif_inv = inv_obj.search(
                [
                    ("state", "=", "draft"),
                    ("journal_id", "=", diff_inv_journal.id),
                    ("partner_id", "=", self.id),
                    ("currency_id", "=", self.env.user.company_id.currency_id.id),
                ]
            )
            if draft_dif_inv:
                for x in draft_dif_inv:
                    x.action_invoice_cancel()

            difference_aml_domain = [
                ("partner_id", "=", self.id),
                ("journal_id", "=", self.company_id.currency_exchange_journal_id.id),
                ("difference_checked", "=", False),
                ("full_reconcile_id", "!=", False),
            ]

            difference_amls = self.env["account.move.line"].search(
                difference_aml_domain
            )
            if (
                difference_amls
                and round(
                    (
                        sum(difference_amls.mapped("debit"))
                        - sum(difference_amls.mapped("credit"))
                    ),
                    2,
                )
                < 0
            ):
                inv_type = "out_refund"
            else:
                inv_type = "out_invoice"
            if difference_amls:
                inv_lines_to_create = []
                comment_einvoice = "Aşağıdaki faturaların kur farkıdır:\n"
                for diff_aml in difference_amls:
                    amount_untaxed = diff_aml.debit or diff_aml.credit
                    inv_line_name = "Kur Farkı"
                    tax_20 = self.env["account.tax"].search(
                        [
                            ("type_tax_use", "=", "sale"),
                            ("amount", "=", 20.0),
                            ("include_base_amount", "=", False),
                        ],
                        limit=1,
                    )
                    tax_10 = self.env["account.tax"].search(
                        [
                            ("type_tax_use", "=", "sale"),
                            ("amount", "=", 10.0),
                            ("include_base_amount", "=", False),
                        ],
                        limit=1,
                    )
                    inv_ids = diff_aml.full_reconcile_id.reconciled_line_ids.filtered(
                        lambda r: r.invoice_id
                    ).mapped("invoice_id")
                    if len(inv_ids) > 0:
                        kdv_20_taxes = sum(
                            inv_ids.mapped("tax_line_ids")
                            .filtered(lambda r: r.tax_id.amount == 20)
                            .mapped("amount")
                        )

                        kdv_10_taxes = sum(
                            inv_ids.mapped("tax_line_ids")
                            .filtered(lambda r: r.tax_id.amount == 10)
                            .mapped("amount")
                        )

                        rate_20 = round(
                            100.0
                            * (kdv_20_taxes / 20.0)
                            / sum(inv_ids.mapped("amount_untaxed")),
                            4,
                        )
                        rate_10 = round(
                            100.0
                            * (kdv_10_taxes / 10.0)
                            / sum(inv_ids.mapped("amount_untaxed")),
                            4,
                        )

                        comment_einvoice += ", ".join(
                            inv_id.supplier_invoice_number
                            if inv_id.supplier_invoice_number
                            else inv_id.number
                            for inv_id in inv_ids
                        )

                        if rate_20 > 0.001:
                            amount_untaxed = round(
                                amount_untaxed * rate_20 / (1 + tax_20.amount / 100.0),
                                2,
                            )
                            tax_ids = [(6, False, [tax_20.id])]

                        if rate_10 > 0.001:
                            amount_untaxed = round(
                                amount_untaxed * rate_10 / (1 + tax_10.amount / 100.0),
                                2,
                            )
                            tax_ids = [(6, False, [tax_10.id])]
                    else:
                        comment_einvoice = ""
                        amount_untaxed = amount_untaxed / (1 + tax_20.amount / 100.0)
                        tax_ids = [(6, False, [tax_20.id])]

                    if inv_type == "out_refund" and diff_aml.debit > 0:
                        amount_untaxed = -amount_untaxed

                    if inv_type == "out_invoice" and diff_aml.credit > 0:
                        amount_untaxed = -amount_untaxed

                    inv_lines_to_create.append(
                        {
                            "difference_base_aml_id": diff_aml.id,
                            "name": inv_line_name,
                            "uom_id": 1,
                            "account_id": self.env.user.company_id.currency_diff_inv_account_id.id,
                            "price_unit": amount_untaxed,
                            "invoice_line_tax_ids": tax_ids,
                        }
                    )

                    diff_aml.write({"difference_checked": True})

                    created_inv_lines = self.env["account.invoice.line"].create(
                        inv_lines_to_create
                    )
                dif_inv = inv_obj.create(
                    {
                        "partner_id": self.id,
                        "date_invoice": date,
                        "journal_id": diff_inv_journal.id,
                        "currency_id": self.env.user.company_id.currency_id.id,
                        "type": inv_type,
                        "billing_point_id": billing_point.id,
                        "payment_term_id": payment_term.id,
                        "comment_einvoice": comment_einvoice,
                    }
                )

                dif_inv.invoice_line_ids = [
                    (6, False, [x.id for x in created_inv_lines])
                ]
                dif_inv._onchange_invoice_line_ids()
                return dif_inv

        return False

    def action_generate_currency_diff_invoice(self):
        view = self.env.ref(
            "currency_difference_invoice.res_partner_create_difference_inv"
        )
        return {
            "name": _("Create Currency Difference Invoice"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "create.currency.difference.invoices",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "context": self.env.context,
        }
