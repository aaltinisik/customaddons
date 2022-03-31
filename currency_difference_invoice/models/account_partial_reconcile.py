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
        total = sum(aml.amount_residual for aml in aml_to_fix)
        created_lines = self.env['account.move.line']
        currency_id = aml_to_fix[0].partner_id.property_account_receivable_id.currency_id
        # amount_in_currency = self.env.user.company_id.currency_id._convert(abs(total), currency_id,
        #                                            self.env.user.company_id,fields.Date.today())
        # create the line that will compensate all the aml_to_fix
        line_to_rec = aml_model.with_context(check_move_validity=False).create({
            'name': _('Currency exchange rate difference'),
            'debit': total < 0 and -total or 0.0,
            'credit': total > 0 and total or 0.0,
            'account_id': aml_to_fix[0].account_id.id,
            'currency_id': currency_id.id,
            'amount_currency': 0.0,
            'move_id': move.id,
            'partner_id': aml_to_fix[0].partner_id.id,
        })
        # create the counterpart on exchange gain/loss account
        exchange_journal = move.company_id.currency_exchange_journal_id
        aml_model.with_context(check_move_validity=False).create({
            'name': _('Currency exchange rate difference'),
            'debit': total > 0 and total or 0.0,
            'credit': total < 0 and -total or 0.0,
            'account_id': total > 0 and exchange_journal.default_debit_account_id.id or exchange_journal.default_credit_account_id.id,
            'move_id': move.id,
            'currency_id': currency_id.id,
            'amount_currency': 0.0,
            'partner_id': aml_to_fix[0].partner_id.id,
        })

        # # reconcile all aml_to_fix
        # partial_rec |= self.create(
        #     self._prepare_exchange_diff_partial_reconcile(
        #         aml=aml,
        #         line_to_reconcile=line_to_rec,
        #         currency=aml.currency_id or False)
        # )
        created_lines |= line_to_rec
        return created_lines
