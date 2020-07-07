# -*- coding: utf-8 -*-
'''
Created on Oct 3, 2019

@author: grey
'''
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def invoice_line_create_vals(self, invoice_id, qty):
        vals_list = super(SaleOrderLine, self).invoice_line_create_vals(invoice_id, qty)
        for vals in vals_list:
            sale_lines = self.browse(vals['sale_line_ids'][0][2])
            move_lines = sale_lines.mapped('move_ids.move_line_ids').filtered(
                lambda m: m.qty_done > sum(l.quantity for l in m.invoice_line_ids.filtered(lambda invl: invl.invoice_id.state != 'cancel')) and m.state=='done')
            if move_lines:
                pickings = move_lines.mapped('picking_id')
                vals.update({'stock_line_ids': [(6, 0, move_lines.ids)],
                             'picking_ids': [(6, 0, pickings.ids)]})
        
        return vals_list
