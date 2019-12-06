# -*- encoding: utf-8 -*-


from odoo import models,api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        res.update({
            'hscode_id': self.product_id.hscode_id.id or self.product_id.categ_id.hscode_id.id,
        })
        return res
