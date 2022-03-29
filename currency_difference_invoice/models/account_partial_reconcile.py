# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountPartialReconcile(models.Model):
    _inherit = 'account.partial.reconcile'

    @api.model
    def create_exchange_rate_entry(self, aml_to_fix, move):
        """
        Automatically create a journal items to book the exchange rate
        differences that can occur in multi-currencies environment. That
        new journal item will be made into the given `move` in the company
        `currency_exchange_journal_id`, and one of its journal items is
        matched with the other lines to balance the full reconciliation.

        :param aml_to_fix: recordset of account.move.line (possible several
            but sharing the same currency)
        :param move: account.move
        :return: tuple.
            [0]: account.move.line created to balance the `aml_to_fix`
            [1]: recordset of account.partial.reconcile created between the
                tuple first element and the `aml_to_fix`
        """
        partial_rec = self.env['account.partial.reconcile']
        aml_model = self.env['account.move.line']

        created_lines = self.env['account.move.line']
        for aml in aml_to_fix:
            #create the line that will compensate all the aml_to_fix
            line_to_rec = aml_model.with_context(check_move_validity=False).create({
                'name': _('Currency exchange rate difference'),
                'debit': aml.amount_residual < 0 and -aml.amount_residual or 0.0,
                'credit': aml.amount_residual > 0 and aml.amount_residual or 0.0,
                'account_id': aml.account_id.id,
                'move_id': move.id,
                'currency_id': aml.currency_id.id,
                'amount_currency': aml.amount_residual_currency and -aml.amount_residual_currency or 0.0,
                'partner_id': aml.partner_id.id,
                'invoice_id': aml.invoice_id.id,
                'payment_id': aml.payment_id.id,
            })
            #create the counterpart on exchange gain/loss account
            exchange_journal = move.company_id.currency_exchange_journal_id
            aml_model.with_context(check_move_validity=False).create({
                'name': _('Currency exchange rate difference'),
                'debit': aml.amount_residual > 0 and aml.amount_residual or 0.0,
                'credit': aml.amount_residual < 0 and -aml.amount_residual or 0.0,
                'account_id': aml.amount_residual > 0 and exchange_journal.default_debit_account_id.id or exchange_journal.default_credit_account_id.id,
                'move_id': move.id,
                'currency_id': aml.currency_id.id,
                'amount_currency': aml.amount_residual_currency and aml.amount_residual_currency or 0.0,
                'partner_id': aml.partner_id.id,
                'invoice_id': aml.invoice_id.id,
                'payment_id': aml.payment_id.id,
            })

            #reconcile all aml_to_fix
            partial_rec |= self.create(
                self._prepare_exchange_diff_partial_reconcile(
                        aml=aml,
                        line_to_reconcile=line_to_rec,
                        currency=aml.currency_id or False)
            )
            created_lines |= line_to_rec
        return created_lines, partial_rec