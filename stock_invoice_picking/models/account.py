# -*- coding: utf-8 -*- 
'''
Created on Nov 8, 2017

@author: dogan
'''
from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    picking_ids = fields.Many2many('stock.picking', compute="_compute_picking_ids",
                                   string='Pickings', store=True)

    @api.depends('invoice_line_ids', 'invoice_line_ids.picking_ids')
    def _compute_picking_ids(self):
        for invoice in self:
            pickings = invoice.invoice_line_ids.mapped('picking_ids')
            invoice.picking_ids = [(6, 0, pickings.ids)]

    @api.multi
    def update_invoice_ref(self):
        self.ensure_one()
        vals = {}
        po_lines = self.invoice_line_ids.mapped('purchase_line_id')
        if po_lines:
            porders = po_lines.mapped('order_id')
            porder_names = ', '.join([order.name or "" for order in porders])
            vals['origin'] = porder_names
            vals['name'] = porder_names
            vals['reference'] = ', '.join([order.partner_ref or "" for order in porders])
            
        so_lines = self.invoice_line_ids.mapped('sale_line_ids')
        if so_lines:
            sorders = so_lines.mapped('order_id')
            vals['origin'] = ', '.join([order.name or "" for order in sorders])
            vals['name'] = ', '.join([order.client_order_ref or order.name or "" for order in sorders])
            
        pickings = self.invoice_line_ids.mapped('move_ids').mapped('picking_id')
        if pickings and not po_lines and not so_lines:
            vals['origin'] = ', '.join([picking.name or "" for picking in pickings])
            vals['name'] = ', '.join([picking.origin or "" for picking in pickings])
        
        self.write(vals)


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    move_ids = fields.Many2many('stock.move', relation='account_invoice_line_stock_move_rel',
                                column1='invoice_line_id', column2='move_id',
                                string='Moves')
    lot_ids = fields.Many2many('stock.production.lot', relation='account_invoice_line_stock_lot_rel',
                               column1='invoice_line_id', column2='lot_id',
                               string='Lots/Serial Numbers')
    moves_picking_ref = fields.Char('Picking Ref', compute="_compute_picking_ref")
    partner_order_ref = fields.Char(string='Order Reference')

    picking_ids = fields.Many2many('stock.picking', compute="_compute_picking_ids",
                                   string='Pickings', store=True)

    @api.depends('move_ids', 'move_ids.picking_id')
    def _compute_picking_ids(self):
        for line in self:
            pickings = line.mapped('move_ids').mapped('picking_id')
            line.picking_ids = [(6, 0, pickings.ids)]

    @api.one
    @api.depends('move_ids', 'move_ids.picking_id')
    def _compute_picking_ref(self):
        pickings = self.move_ids.mapped('picking_id')
        self.moves_picking_ref = ', '.join([picking.name or "" for picking in pickings])
