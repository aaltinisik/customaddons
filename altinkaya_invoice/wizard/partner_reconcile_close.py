# -*- encoding: utf-8 -*-
#
# Created on Dec 4, 2018
#
# @author: dogan
#

from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class PartnerReconcileClose(models.TransientModel):
    """
    Wizard for reconciliation of account move lines and creating closing/opening moves
    """

    _name = "partner.reconcile.close"
    _description = "Partner Reconcile Close"

    country_id = fields.Many2one("res.country", string="Partner Country")
    customer = fields.Boolean("Customer")
    supplier = fields.Boolean("Supplier")
    partner_id = fields.Many2one("res.partner", string="Partner")
    try_journal_id = fields.Many2one(
        "account.journal", string="Transfer Journal TRY", required=True
    )
    usd_journal_id = fields.Many2one(
        "account.journal", string="Transfer Journal USD", required=True
    )
    eur_journal_id = fields.Many2one(
        "account.journal", string="Transfer Journal EUR", required=True
    )
    try_account_id = fields.Many2one(
        "account.account", string="TRY Transfer Account", required=True
    )
    usd_account_id = fields.Many2one(
        "account.account", string="USD Transfer Account", required=True
    )
    eur_account_id = fields.Many2one(
        "account.account", string="EUR Transfer Account", required=True
    )
    transfer_description = fields.Char("Transfer description", required=True)
    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)
    opening_move_date = fields.Date("Opening Move Date", required=True)
    closing_move_date = fields.Date("Closing Move Date", required=True)
    batch_size = fields.Integer("Batch Size", default=1000)

    @api.onchange("country_id", "customer", "supplier")
    def onchange_country_id(self):
        domain = []
        if self.country_id:
            domain.append(("country_id", "=", self.country_id.id))

        if self.customer and not self.supplier:
            domain.append(("customer", "=", True))

        if not self.customer and self.supplier:
            domain.append(("supplier", "=", True))

        if self.customer and self.supplier:
            domain.extend(["|", ("customer", "=", True), ("supplier", "=", True)])

        return {"domain": {"partner_id": domain}}

    @api.multi
    def action_done(self):

        self.ensure_one()
        domain = [
            ("date", ">=", self.start_date),
            ("date", "<=", self.end_date),
            ("reconciled", "=", False),
            ("full_reconcile_id", "=", False),
        ]
        partner_ids = self.env["res.partner"]
        move_obj = self.env["account.move"]
        move_line_obj = self.env["account.move.line"].with_context(
            {"comment": self.transfer_description}
        )
        if self.partner_id:
            partner_ids |= self.partner_id
        else:
            partner_domain = [("parent_id", "=", False), ("devir_yapildi", "=", False)]

            if self.country_id:
                partner_domain.append(("country_id", "=", self.country_id.id))

            if self.customer and not self.supplier:
                partner_domain.append(("customer", "=", True))

            if not self.customer and self.supplier:
                partner_domain.append(("supplier", "=", True))

            if self.customer and self.supplier:
                partner_domain.extend(
                    ["|", ("customer", "=", True), ("supplier", "=", True)]
                )

            partner_ids = self.env["res.partner"].search(
                partner_domain, limit=self.batch_size
            )
        move_mapping = {}
        for journal in partner_ids.mapped("partner_currency_id.name"):
            journal = journal.lower()
            # vade tarihi yapılacak todo:
            move_mapping[journal] = {
                "opening_move_id": move_obj.create(
                    {
                        "journal_id": getattr(self, f"{journal}_journal_id").id,
                        "date": self.closing_move_date,
                        "state": "draft",
                        "currency_id": self.env.ref(f"base.{journal.upper()}").id,
                    }
                ),
                "closing_move_id": move_obj.create(
                    {
                        "journal_id": getattr(self, f"{journal}_journal_id").id,
                        "date": self.opening_move_date,
                        "state": "draft",
                        "currency_id": self.env.ref(f"base.{journal.upper()}").id,
                    }
                ),
                "account_id": getattr(self, f"{journal}_account_id").id,
            }

        for partner in partner_ids.filtered(lambda p: not p.devir_yapildi):
            try:

                for account in [
                    partner.property_account_receivable_id,
                    partner.property_account_payable_id,
                ]:
                    currency_id = account.currency_id or account.company_id.currency_id
                    target_account_id = move_mapping[currency_id.name.lower()][
                        "account_id"
                    ]
                    closing_move_id = move_mapping[currency_id.name.lower()][
                        "closing_move_id"
                    ]
                    opening_move_id = move_mapping[currency_id.name.lower()][
                        "opening_move_id"
                    ]
                    lines = move_line_obj.search(
                        domain
                        + [
                            ("partner_id", "=", partner.id),
                            ("account_id", "=", account.id),
                        ]
                    )
                    if len(lines) == 0:
                        _logger.info(
                            "Partner already reconciled: %s" % partner.name
                        )
                        continue
                    balance = sum([ml.debit - ml.credit for ml in lines])
                    date_due = max(lines.mapped("date_maturity"))
                    amount_currency = sum(lines.mapped("amount_currency"))
                    if balance > 0:
                        debit = balance
                        credit = 0.0
                        self_credit = balance
                        self_debit = 0.0
                    elif balance < 0:
                        debit = 0.0
                        credit = -balance
                        self_credit = 0.0
                        self_debit = -balance
                    else:
                        continue

                    lines |= closing_move_id.line_ids.create(
                        [
                            {
                                "move_id": closing_move_id.id,
                                "name": _("Closing"),
                                "debit": self_debit,
                                "credit": self_credit,
                                "account_id": account.id,
                                "amount_currency": -amount_currency,
                                "date": self.closing_move_date,
                                "date_maturity": date_due,
                                "partner_id": partner.id,
                                "currency_id": (account.currency_id.id or False),
                            },
                            {
                                "move_id": closing_move_id.id,
                                "name": _("Closing"),
                                "debit": debit,
                                "credit": credit,
                                "amount_currency": amount_currency,
                                "account_id": account.id,
                                "date": self.closing_move_date,
                                "date_maturity": date_due,
                                "partner_id": partner.id,
                                "currency_id": (account.currency_id.id or False),
                            },
                        ]
                    )

                    opening_move_id.line_ids.create(
                        [
                            {
                                "move_id": opening_move_id.id,
                                "name": _("Opening"),
                                "debit": debit,
                                "credit": credit,
                                "amount_currency": amount_currency,
                                "account_id": account.id,
                                "date": self.opening_move_date,
                                "date_maturity": date_due,
                                "partner_id": partner.id,
                                "currency_id": (account.currency_id.id or False),
                            },
                            {
                                "move_id": opening_move_id.id,
                                "name": _("Opening"),
                                "debit": self_debit,
                                "credit": self_credit,
                                "amount_currency": -amount_currency,
                                "account_id": target_account_id,
                                "date": self.opening_move_date,
                                "date_maturity": date_due,
                                "partner_id": partner.id,
                                "currency_id": (account.currency_id.id or False),
                            },
                        ]
                    )
                    lines.remove_move_reconcile()
                    lines.reconcile()
                    _logger.info(
                        "Partner reconcilation done. Partner: %s \n\n" % partner.name
                    )
                partner.devir_yapildi = True
                self._cr.commit()

            except Exception as e:
                _logger.exception(
                    "Partner reconciliation wizard error. Partner: %s \n\n %s"
                    % (partner.name, e)
                )
        for move_map in move_mapping.values():
            closing_move_id = move_map["closing_move_id"]
            opening_move_id = move_map["opening_move_id"]
            closing_move_id.post()
            opening_move_id.post()

        # return {"type": "ir.actions.act_window_close"}
