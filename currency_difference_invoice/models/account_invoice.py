# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def register_payment(self, payment_line, writeoff_acc_id=False, writeoff_journal_id=False):

        if not self:
            return True
        for aml in payment_line:
            aml.write({'invoice_id': self.id})
        return super(AccountInvoice, self).register_payment(payment_line, writeoff_acc_id=writeoff_acc_id,
                                                            writeoff_journal_id=writeoff_journal_id)

    @api.multi
    def action_invoice_open(self):
        """
        Override method to check if the invoice is in the same currency as the
        company currency.
        """
        res = super(AccountInvoice, self).action_invoice_open()

        if not self:
            return res

        for invoice in self:
            moves_to_reconcile = self.env['account.move.line']
            for inv_line in invoice.invoice_line_ids:
                moves_to_reconcile |= inv_line.mapped('moves_to_reconcile').filtered(lambda r: r.reconciled is True)

            if moves_to_reconcile:
                moves_to_reconcile.remove_move_reconcile()
                # reconcile difference invoice lines with the previously calculated move lines to reconcile
                moves_to_reconcile |= invoice.move_id.line_ids.filtered(
                    lambda r: not r.reconciled and r.account_id.reconcile)
                moves_to_reconcile.reconcile()


    @api.multi
    def action_invoice_cancel(self):
        res = super(AccountInvoice, self).action_invoice_cancel()

        if not self:
            return res

        for invoice in self:
            if invoice.invoice_line_ids and invoice.journal_id == self.env.user.company_id.currency_exchange_journal_id:
                for line in invoice.invoice_line_ids:
                    for aml in line.mapped('difference_base_move_id'):
                        aml.write({'difference_checked': False})

    @api.multi
    def unlink(self):
        for invoice in self:
            if invoice.invoice_line_ids and invoice.journal_id == self.env.user.company_id.currency_exchange_journal_id:
                for line in invoice.invoice_line_ids:
                    for aml in line.mapped('difference_base_move_id'):
                        aml.write({'difference_checked': False})

        return super(AccountInvoice, self).unlink()
