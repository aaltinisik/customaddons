# -*- coding: utf-8 -*- 
'''
Created on Aug 25, 2017

@author: dogan
'''

from odoo import models, api, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    invoice_ids = fields.Many2many('account.invoice', compute="_compute_invoice_ids",
                                   string='Invoices', store=True)
    invoice_count = fields.Integer('Invoices', compute="_compute_invoice_ids")
    invoice_status = fields.Selection([
        ('no','Nothing to Invoice'),
        ('to_invoice','To Invoice'),
        ('invoiced','Invoiced')
        ], string='Invoice Status', compute="_compute_invoice_status", store=True, readonly=True, default='no')
    
    @api.depends('move_lines', 'move_lines.invoice_status')
    def _compute_invoice_status(self):
        for picking in self:
            if any(line.invoice_status == 'to_invoice' for line in picking.move_lines):
                picking.invoice_status = 'to_invoice'
            elif all(line.invoice_status == 'invoiced' for line in picking.move_lines):
                picking.invoice_status = 'invoiced'
            else:
                picking.invoice_status = 'no'
    
    @api.depends('move_lines', 'move_lines.invoice_line_ids', 'move_lines.invoice_line_ids.invoice_id')
    def _compute_invoice_ids(self):
        for picking in self:
            invoices = picking.move_lines.mapped('invoice_line_ids').mapped('invoice_id')
            picking.invoice_ids = [(6, 0, invoices.ids)]
            picking.invoice_count = len(invoices.filtered(lambda x:x.state != 'cancel'))

    @api.multi
    def action_view_invoice(self):
        self.ensure_one()
        if self.picking_type_id.code == 'outgoing':
            action_ref = 'account.action_invoice_tree1'
            form_view_ref = 'account.invoice_form'
        else:
            action_ref = 'account.action_invoice_tree2'
            form_view_ref = 'account.invoice_supplier_form'
        action = self.env.ref(action_ref).read()[0]
        invoices = self.invoice_ids
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif invoices:
            action['views'] = [(self.env.ref(form_view_ref).id, 'form')]
            action['res_id'] = invoices[0].id or False
        return action
