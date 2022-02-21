# -*- coding: utf-8 -*- 
'''
Created on Nov 8, 2017

@author: dogan
'''
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class StockPickingCreateInvoice(models.TransientModel):
    _name = 'stock.picking.create_invoice'
    _description="Create Invoice From Stock"
    
    @api.model
    def default_get(self, fields):
        res = super(StockPickingCreateInvoice, self).default_get(fields)
        context = self._context
        if context and context.get('active_model') == 'stock.picking' and context.get('active_ids'):
            pickings = self.env['stock.picking'].search([('id','in',self._context.get('active_ids')),('state','=','done')])
            if pickings:
                if len(pickings.mapped('partner_id').mapped('commercial_partner_id')) != 1:
                    raise UserError(_('All transfers must be linked to a single commercial partner.'))
                if len(pickings.mapped('picking_type_id')) != 1 and len(pickings.mapped('company_id')) != 1:
                    raise UserError(_('All transfer types must be same to merge invoice'))
                
                all_moves = pickings.mapped('move_lines')
                so_lines = all_moves.mapped('sale_line_id')
                po_lines = all_moves.mapped('purchase_line_id')
                if so_lines and not po_lines:
                    invoice_type = 'sale'
                elif po_lines and not so_lines:
                    invoice_type = 'purchase'
                else:
                    invoice_type = 'transfer'
                
                if invoice_type == 'sale' and len(so_lines.mapped('currency_id')) == 1:
                    currency_id = so_lines.mapped('currency_id')
                elif invoice_type == 'purchase' and len(po_lines.mapped('currency_id')) == 1:
                    currency_id = po_lines.mapped('currency_id')
                elif invoice_type != 'transfer':
                    raise UserError(_('Currency Error: Multiple currency or No currency!'))
                if invoice_type == 'transfer':
                    currency_id = pickings[0].company_id.currency_id
    
                invoice_journal = self.env['account.invoice'].default_get(['journal_id'])['journal_id']
                invoice_journal_id = self.env['account.journal'].browse(invoice_journal)
                invoice_partner_id = pickings and pickings[0].partner_id.commercial_partner_id
                if invoice_type == 'sale':
                    if len(so_lines.mapped('order_id')) == 1:
                        invoice_partner_id = so_lines.mapped('order_id').partner_invoice_id
                    elif len(so_lines.mapped('order_id').mapped('partner_invoice_id')) == 1:
                        invoice_partner_id = so_lines.mapped('order_id').mapped('partner_invoice_id')
                elif invoice_type == 'purchase':
                    if len(po_lines.mapped('order_id')) == 1:
                        invoice_partner_id = po_lines.mapped('order_id').partner_id
                    journal_domain = [
                        ('type', '=', 'purchase'),
                        ('company_id', '=', pickings.mapped('company_id').id),
                        ('currency_id', '=', currency_id.id),
                    ]
                    invoice_journal_id = self.env['account.journal'].search(journal_domain, limit=1)
                    if not invoice_journal_id:
                        journal_domain = [('type', '=', 'purchase'),('company_id', '=', pickings.mapped('company_id').id)]
                        invoice_journal_id = self.env['account.journal'].search(journal_domain, limit=1)
                
                res['invoice_type'] = invoice_type
                res['journal_id'] = invoice_journal_id.id
                res['currency_id'] = currency_id.id
                res['commercial_partner_id'] = invoice_partner_id.commercial_partner_id.id
                res['partner_invoice_id'] = invoice_partner_id.id
            else:
                raise UserError(_('No found transfer'))
        return res
    
    date_invoice = fields.Date('Invoice Date')
    currency_id = fields.Many2one('res.currency', string='Invoice Currency')
    partner_invoice_id = fields.Many2one('res.partner', string='Invoice Address', required=True)
    commercial_partner_id = fields.Many2one('res.partner', string='Commercial Partner')
    journal_id = fields.Many2one('account.journal', string='Journal', required=True)
    invoice_type = fields.Char('Invoice Type')

    def wizard_update_invoice_data(self, inv_data):
        inv_data.update({
            'date_invoice': self.date_invoice,
            'journal_id': self.journal_id.id,
            'partner_id': self.partner_invoice_id.id
            })
        return inv_data

    def _get_partner_property_account_id(self, picking):
        partner = self.partner_invoice_id
        partner_account_id = False
        if picking.picking_type_id.code == 'outgoing':
            partner_account_id = partner.property_account_receivable_id
        elif picking.picking_type_id.code == 'incoming':
            partner_account_id = partner.property_account_payable_id
        if not partner_account_id:
            raise UserError(_('Please, check picking type!'))
        return partner_account_id

    def _prepare_invoice(self, picking):
        account_id = self._get_partner_property_account_id(picking)
        journal_id = self.journal_id
        name = picking.origin or ''
        reference = False
        inv_type = 'out_invoice'
        if self.invoice_type == 'sale':
            name = picking.sale_id.client_order_ref or ""
        elif self.invoice_type == 'purchase':
            reference = picking.purchase_id.partner_ref
            inv_type = 'in_invoice'
            
        invoice_vals = {
            'name': name,
            'reference': reference,
            'origin': picking.name,
            'carrier_id': picking.carrier_id.id,
            'address_contact_id': picking.partner_id.id,
            'type': inv_type,
            'account_id': account_id.id,
            'partner_id': self.partner_invoice_id.id,
            'partner_shipping_id': picking.partner_id.id,
            'journal_id': journal_id,
            'pricelist_id': picking.sale_id.pricelist_id.id or False,
            'currency_id': self.currency_id.id,
            'comment': picking.note,
            'fiscal_position_id': self.partner_invoice_id.property_account_position_id.id or False,
            'company_id': picking.company_id.id,
            'user_id': self.env.user.id,
        }
        return invoice_vals

    @api.multi
    def create_invoices(self):
        self.ensure_one()
        pickings = self.env['stock.picking'].search([('id','in',self._context.get('active_ids')),('state','=','done')])
        
        invoices = {}
        references = {}
        for picking in pickings:
            group_key = (self.invoice_type, self.partner_invoice_id, self.currency_id)
            if group_key not in invoices.keys():
                inv_data = self._prepare_invoice(picking)
                inv_data = self.wizard_update_invoice_data(inv_data)
                new_invoice = self.env['account.invoice'].create(inv_data)
                invoices[group_key] = new_invoice
                references[invoices[group_key]] = picking
            
            for move in picking.move_lines.filtered(lambda m:m.state=='done'):
                inv_line_data = move.with_context(date=self.date_invoice).prepare_invoice_line(self.partner_invoice_id)
                lots=move.move_line_ids.mapped('lot_id')
                inv_line_data.update({'invoice_id': invoices[group_key].id,
                                      'lot_ids': [(4, lot.id) for lot in lots]})
                invoice_line = self.env['account.invoice.line'].create(inv_line_data)
                move.invoice_line_ids = [(4, invoice_line.id, None)]

            if references.get(invoices.get(group_key)):
                if picking not in references[invoices[group_key]]:
                    references[invoices[group_key]] = references[invoices[group_key]] | picking

            invoices[group_key].update_invoice_ref()

        for invoice in invoices.values():
            for line in invoice.invoice_line_ids:
                line._set_additional_fields(invoice)
            # Necessary to force computation of taxes. In account_invoice, they are triggered
            # by onchanges, which are not triggered when doing a create.
            invoice.compute_taxes()
            invoice.message_post_with_view('mail.message_origin_link',
                values={'self': invoice, 'origin': references[invoice]},
                subtype_id=self.env.ref('mail.mt_note').id)
        
#         return [inv.id for inv in invoices.values()]
        return {'type': 'ir.actions.act_window_close'}
