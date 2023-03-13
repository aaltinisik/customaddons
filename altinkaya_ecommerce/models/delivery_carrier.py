# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, api, _


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    def rate_shipment(self, order):
        """
        Override rate_shipment method to use external rate
        """
        self.ensure_one()
        odoo_carrier = self.env["odoo.delivery.carrier"].search(
            [("odoo_id", "=", self.id)]
        )
        if not odoo_carrier:
            return super().rate_shipment(order)
        vals = {
            "success": False,
            "price": 0.0,
            "warning_message": "",
            "error_message": "",
        }
        res = odoo_carrier._get_external_rate(order)
        if res:
            vals["success"] = True
            vals["price"] = res
        else:
            vals["error_message"] = _("No rate found for this address.")
        return vals
