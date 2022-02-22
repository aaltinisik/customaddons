

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleConfirmPayment(models.TransientModel):
    _name = "sale.confirm.payment"
    _description = "Sale Confirm Payment"

    transaction_id = fields.Many2one("payment.transaction", readonly=True)
    acquirer_id = fields.Many2one("payment.acquirer", required=True)
    amount = fields.Monetary(string="Amount", required=True)
    currency_id = fields.Many2one("res.currency")
    payment_date = fields.Date(string="Payment Date", required=True, default=fields.Date.context_today)
    order_id = fields.Many2one(comodel_name="sale.order")
    order_state = fields.Selection(
        related='order_id.state', readonly=True, store=True,
        string="State")

    # @api.one
    # @api.depends('transaction_id')
    # def _compute_sale_id(self):
    #     active_id = self.env.context.get("active_id", False)
    #     self.order_id = self.env["sale.order"].browse(active_id)

    @api.model
    def default_get(self, fields_list):
        defaults = super(SaleConfirmPayment, self).default_get(fields_list)
        active_id = self.env.context.get("active_id", False)
        if not active_id:
            raise UserError(_("Please select a sale order"))

        order = self.env["sale.order"].browse(active_id)
        defaults["currency_id"] = order.currency_id.id
        defaults['order_id'] = active_id

        tx = order.sudo().transaction_ids.get_last_transaction()
        if tx and tx.state in ["pending", "authorized"]:
            defaults["transaction_id"] = tx.id
            defaults["acquirer_id"] = tx.acquirer_id.id
            defaults["amount"] = tx.amount

        return defaults

    def do_confirm(self):

        if self.amount <= 0:
            raise UserError(_("Then amount must be positive"))

        if self.transaction_id and self.transaction_id.amount == self.amount:
            transaction = self.transaction_id
        else:
            transaction = self.env["payment.transaction"].create(
                {
                    "amount": self.amount,
                    "acquirer_id": self.acquirer_id.id,
                    "acquirer_reference": self.order_id.name,
                    "partner_id": self.order_id.partner_id.id,
                    "sale_order_ids": [(4, self.order_id.id, False)],
                    "currency_id": self.currency_id.id,
                    "date": self.payment_date,
                    "state": "draft",
                }
            )

        if transaction.state != "done":
            transaction = transaction.with_context(payment_date=self.payment_date)
            transaction._set_transaction_pending()
            transaction._set_transaction_done()
            transaction._post_process_after_done()
        if transaction:
            self.order_id.payment_ids = [(4, transaction.payment_id.id)]
        return transaction

    def add_payment_and_confirm(self):
        transaction = self.do_confirm()
        active_id = self.env.context.get("active_id", False)
        if not active_id:
            raise UserError(_("Please select a sale order"))
        if self.order_id.state not in ['done', 'cancel']:
            self.order_id.action_confirm()
        return transaction

    def print_report(self):
        transaction = self.add_payment_and_confirm()
        data = {
            'ids': transaction.payment_id.id,
            'doc_ids': transaction.payment_id.id,
            'model': 'account.payment',
            'doc_model': self.env['account.payment']._name,
            'form': transaction.payment_id.read()[0]}
        return self.env.ref('account.action_report_payment_receipt'). \
            with_context(active_model='account.payment').report_action(docids=data['doc_ids'])
