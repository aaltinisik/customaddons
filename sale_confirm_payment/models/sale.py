from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    acquirer_id = fields.Many2one("payment.acquirer", related="transaction_ids.acquirer_id", store=True)
    payment_amount = fields.Monetary(string="Amount Payment", compute="_compute_payment")
    payment_ids = fields.Many2many('account.payment', string='Payments', readonly=True)

    payment_status = fields.Selection(
        [
            ("without", "Without"),
            ("initiated", "Initiated"),
            ("authorized", "Authorized"),
            ("partial", "Partial"),
            ("done", "Done"),
        ],
        default="without",
        compute="_compute_payment",
        store=True,
    )

    @api.multi
    def action_confirm_payment(self):
        aw_obj = self.env['ir.actions.act_window']
        action = aw_obj.for_xml_id('sale_confirm_payment', 'action_confirm_payment_sale')
        return action

    @api.depends("transaction_ids")
    def _compute_payment(self):
        for order in self:

            amount = 0
            transactions = order.sudo().transaction_ids.filtered(lambda a: a.state == "done")
            for invoice in order.invoice_ids:
                amount += invoice.amount_total - invoice.residual
                transactions = transactions - invoice.transaction_ids
            for transaction in transactions:
                amount += transaction.amount
            order.payment_amount = amount
            if amount:
                if amount < order.amount_total:
                    order.payment_status = "partial"
                else:
                    order.payment_status = "done"

            if not amount:
                order.payment_status = "without"
                if order.transaction_ids:
                    order.payment_status = "initiated"
                    authorized_transaction_ids = order.transaction_ids.filtered(lambda t: t.state == "authorized")
                    if authorized_transaction_ids:
                        order.payment_status = "authorized"

