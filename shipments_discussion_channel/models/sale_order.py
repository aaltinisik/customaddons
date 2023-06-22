from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.state == "sale":
            for order in self:
                if order.partner_id.country_id.id != 224:  # 224=Turkey (res.country)
                    channel = self.env["mail.channel"].search(
                        [("name", "=", "Approved Shipments")]
                    )
                    if channel:
                        channel.message_post(
                            body=f"Export shipment {order.name} approved!",
                            message_type="comment",
                            subtype="mail.mt_comment",
                        )
        return res
