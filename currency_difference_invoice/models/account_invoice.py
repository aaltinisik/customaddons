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
        For currency difference Invoices Override method to unreconcile previous account move lines and
        reconcie new account move lines
        """
        res = super(AccountInvoice, self).action_invoice_open()

        if not self:
            return res

        for invoice in self:
            aml_to_unreconcile = self.env['account.move.line']
            aml_to_reconcile = self.env['account.move.line']
            for inv_line in invoice.invoice_line_ids.filtered(lambda x: x.difference_base_aml_id):

                aml_to_unreconcile |= inv_line.difference_base_aml_id.full_reconcile_id.reconciled_line_ids
                aml_to_reconcile |= inv_line.difference_base_aml_id.full_reconcile_id.reconciled_line_ids.filtered(lambda r: r.id != inv_line.difference_base_aml_id.id)

            if aml_to_unreconcile:
                aml_to_unreconcile.remove_move_reconcile()

            if aml_to_reconcile:
                diff_aml = invoice.move_id.line_ids.filtered(lambda r: not r.reconciled and
                                                                          r.account_id.internal_type in
                                                                          ('payable', 'receivable'))
                aml_to_reconcile._reconcile(diff_aml=diff_aml)



    @api.multi
    def action_invoice_cancel(self):
        res = super(AccountInvoice, self).action_invoice_cancel()

        if not self:
            return res

        for invoice in self:
            if invoice.invoice_line_ids and invoice.journal_id.code == 'KFARK':
                for line in invoice.invoice_line_ids.filtered(lambda x: x.difference_base_aml_id):
                    line.difference_base_aml_id.write({'difference_checked': False})


    @api.multi
    def unlink(self):
        for invoice in self:
            if invoice.invoice_line_ids and invoice.journal_id.code == 'KFARK':
                for line in invoice.invoice_line_ids.filtered(lambda x: x.difference_base_aml_id):
                    line.difference_base_aml_id.write({'difference_checked': False})

        return super(AccountInvoice, self).unlink()
