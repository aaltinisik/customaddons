# -*- coding: utf-8 -*- 
'''
Created on Aug 25, 2017

@author: dogan
'''

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare
from odoo.addons import decimal_precision as dp


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    invoice_line_ids = fields.Many2many('account.invoice.line', relation='stock_move_invoice_line_rel',
                                        column1='move_id', column2='invoice_line_id',
                                        string='Invoice Line', copy=False)
    invoice_status = fields.Selection([
        ('no','Nothing to Invoice'),
        ('to_invoice','To Invoice'),
        ('invoiced','Invoiced')
        ],string='Invoice Status', compute="_compute_invoice_status", store=True, readonly=True, default='no')

    qty_to_invoice = fields.Float(
        compute='_get_to_invoice_qty', string='To Invoice', store=True, readonly=True,
        digits=dp.get_precision('Product Unit of Measure'))
    qty_invoiced = fields.Float(
        compute='_get_invoice_qty', string='Invoiced', store=True, readonly=True,
        digits=dp.get_precision('Product Unit of Measure'))
    
    allow_to_invoice = fields.Boolean('Is Invoiceable?', default=True)

    @api.depends('invoice_line_ids.invoice_id.state', 'invoice_line_ids.quantity')
    def _get_invoice_qty(self):
        for move in self:
            qty_invoiced = 0.0
            for invoice_line in move.invoice_line_ids:
                if invoice_line.invoice_id.state != 'cancel':
                    qty_invoiced += invoice_line.uom_id._compute_quantity(invoice_line.quantity, move.product_uom)
            move.qty_invoiced = qty_invoiced

    @api.depends('qty_invoiced', 'product_uom_qty', 'state', 'allow_to_invoice')
    def _get_to_invoice_qty(self):
        for move in self:
            if not move.allow_to_invoice:
                move.qty_to_invoice = 0.0
            elif move.state in ['assigned', 'done'] and (move.product_uom_qty > move.qty_invoiced):
                move.qty_to_invoice = move.product_uom_qty - move.qty_invoiced
            else:
                move.qty_to_invoice = 0.0

    @api.depends('state', 'product_uom_qty', 'qty_to_invoice', 'qty_invoiced', 'allow_to_invoice')
    def _compute_invoice_status(self):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for move in self:
            if not float_is_zero(move.qty_invoiced, precision_digits=precision) and not move.allow_to_invoice:
                move.invoice_status = 'invoiced'
            elif move.state not in ('done') or not move.allow_to_invoice:
                move.invoice_status = 'no'
            elif not float_is_zero(move.qty_to_invoice, precision_digits=precision):
                move.invoice_status = 'to_invoice'
#             elif move.state == 'sale' and move.product_id.invoice_policy == 'order' and\
#                     float_compare(move.qty_delivered, move.product_uom_qty, precision_digits=precision) == 1:
#                 move.invoice_status = 'upselling'
            elif float_compare(move.qty_invoiced, move.product_uom_qty, precision_digits=precision) >= 0:
                move.invoice_status = 'invoiced'
            else:
                move.invoice_status = 'no'


    def _product_property_account_id(self, product, inv_type):
        product_account_id = False
        if inv_type == 'out_invoice':
            product_account_id = product.property_account_income_id or self.product_id.categ_id.property_account_income_categ_id
        elif inv_type == 'in_invoice':
            product_account_id = product.property_account_expense_id or self.product_id.categ_id.property_account_expense_categ_id
        return product_account_id

    @api.multi
    def prepare_invoice_line(self, partner_id):
        self.ensure_one()
        if self.picking_id.picking_type_id.code == 'outgoing':
            account = self._product_property_account_id(self.product_id, 'out_invoice')
        elif self.picking_id.picking_type_id.code == 'incoming':
            account = self._product_property_account_id(self.product_id, 'in_invoice')
        else:
            account = self._product_property_account_id(self.product_id, 'out_invoice')
            
        if not account:
            raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))

        fpos = partner_id.property_account_position_id
        if fpos:
            account = fpos.map_account(account)
            
        sale_line = self.sale_line_id
        po_line = self.purchase_line_id
        if sale_line:
            fpos = sale_line.order_id.fiscal_position_id
            if fpos:
                account = fpos.map_account(account)
        elif po_line:
            invoice_line = self.env['account.invoice.line']
            po_account = invoice_line.get_invoice_line_account('in_invoice', po_line.product_id, po_line.order_id.fiscal_position_id, self.env.user.company_id)
            if po_account:
                account = po_account

        vals = {
            'move_ids': [(4, self.id, None)],
            'name': self.product_id.name,
            'sequence': self.sequence,
            'origin': self.name,
            'account_id': account.id,
            'price_unit': 0.0,
            'quantity': self.qty_to_invoice,
            'discount': 0.0,
            'uom_id': self.product_uom.id,
            'product_id': self.product_id.id or False,
            'invoice_line_tax_ids': False,
            'account_analytic_id': False,
            'analytic_tag_ids': False,
            'sale_line_ids': False,
            'partner_order_ref': False,
            'purchase_line_id': False,
        }
        
        if sale_line:
            vals.update({
                'name': sale_line.name,
                'sequence': sale_line.sequence,
                'origin': sale_line.order_id.name,
                'price_unit': sale_line.price_unit,
                'discount': sale_line.discount,
                'invoice_line_tax_ids': [(6, 0, sale_line.tax_id.ids)],
                'account_analytic_id': sale_line.order_id.analytic_account_id and sale_line.order_id.analytic_account_id.id or False,
                'analytic_tag_ids': [(6, 0, sale_line.analytic_tag_ids.ids)],
                'sale_line_ids': [(6, 0, [sale_line.id])],
                'partner_order_ref': sale_line.order_id.client_order_ref or sale_line.order_id.name or ""
                })
            
        if po_line:
#             vals = self._prepare_invoice_line_from_po_line
            taxes = po_line.taxes_id
            invoice_line_tax_ids = po_line.order_id.fiscal_position_id.map_tax(taxes)
            vals.update({
                'purchase_line_id': po_line.id,
                'name': po_line.order_id.name+': '+po_line.name,
                'origin': po_line.order_id.origin,
                'price_unit': po_line.order_id.currency_id.compute(po_line.price_unit, invoice_line.invoice_id.currency_id, round=False),
                'discount': 0.0,
                'account_analytic_id': po_line.account_analytic_id and po_line.account_analytic_id.id or False,
                'analytic_tag_ids': po_line.analytic_tag_ids and po_line.analytic_tag_ids.ids or False,
                'invoice_line_tax_ids': [(6, 0, invoice_line_tax_ids.ids)],
                'partner_order_ref': po_line.order_id.partner_ref or po_line.order_id.name or "",
                })

        return vals
