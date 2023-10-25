# © 2016 ADHOC SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def register_payment(
        self, payment_line, writeoff_acc_id=False, writeoff_journal_id=False
    ):
        """
        With this we arrange that payments can be paid against a non-reconcilable account.
        account, we fix this because odoo sends to reconcile even if there are no invoices
        there are no invoices and it gives an error, so if there are no invoices
        """
        if not self:
            return True
        return super(AccountInvoice, self).register_payment(
            payment_line,
            writeoff_acc_id=writeoff_acc_id,
            writeoff_journal_id=writeoff_journal_id,
        )
