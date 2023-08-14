from odoo import models, api


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    @api.multi
    def _post_process_after_done(self):
        res = super(PaymentTransaction, self)._post_process_after_done()
        for tx in self.filtered(lambda t: t.sale_order_ids and t.payment_id):
            tx.sale_order_ids.payment_ids = [(4, tx.payment_id.id)]
            tx.sale_order_ids._compute_payment_state()
        return res
