# -*- encoding: utf-8 -*-
'''
Created on Jan 16, 2019

@author: Codequarters
'''
from odoo import models,fields,api
from werkzeug import url_encode
import hashlib


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    #altinkaya61
    x_comment_export = fields.Text('ihracaat fatura notu')
    z_tevkifatli_mi = fields.Boolean(';TEVKiFATLI', help="Eger fatura tevkifatli fatura ise bu alan secilmeli Sadece zirve programi transferinde kullanilmaktadir.")

    carrier_id = fields.Many2one('delivery.carrier', 'Carrier')
       
    x_serino = fields.Char('Fatura No',size=64)
    x_teslimat = fields.Char('Teslimat Kisaltmasi',size=64)
    address_contact_id = fields.Many2one('res.partner','Shipping Address')
    altinkaya_payment_url = fields.Char(compute='_compute_altinkaya_payment_url', string='Altinkaya Payment Url')
    receiver = fields.Char(string="Reciever")
    
    #TODO this is not required we can use invoice.number field for supplier invoices
    supplier_invoice_number = fields.Char(string='Supplier Invoice Number',
        help="The reference of this invoice as provided by the supplier.",
        readonly=True, states={'draft': [('readonly', False)]})
    
    waiting_picking_ids = fields.One2many('stock.picking', string="Waiting Pickings",
                                          compute="_compute_waiting_picking_ids")

    def _compute_waiting_picking_ids(self):
        
        stocks = self.env['stock.picking'].search([('partner_id', '=', self.partner_id.id),
                                                   ('picking_type_id.code', '=', 'incoming'),
                                                   ('invoice_state', '=', '2binvoiced')])
        
        return stocks
    
    
    #TDE Fix Onur
    #invoice have picking_ids but not yet
    @api.multi
    def invoice_validate(self):
        res = super(AccountInvoice, self).invoice_validate()
        user = self.env['res.users'].browse(self.env.user.id)
        for invoice in self:
            for picking in invoice.picking_ids:
                if picking.carrier_id.id != invoice.carrier_id.id:
                    picking.message_post(body='Carrier changed from %s to %s through invoice by %s' % (picking.carrier_id.name,invoice.carrier_id.name, user.name))
                    picking.write({'carrier_id':invoice.carrier_id.id})
           
        return res
    
    @api.depends('amount_total','partner_id','currency_id')
    def _compute_altinkaya_payment_url(self):
        for invoice in self:
            tutar = '%d' % (int)(100*invoice.amount_total)
            eposta = invoice.partner_id.email
            if eposta is False:
                eposta = ""
            params = {
                    "email": eposta,
                    "musteri": invoice.partner_id.commercial_partner_id.name,
                    "oid": invoice.number,
                    "tutar": tutar,
                    "ref": invoice.partner_id.commercial_partner_id.ref,
                    "currency": invoice.currency_id.name,
                    "lang": invoice.partner_id.lang,
                    "hashtr": hashlib.sha1(invoice.currency_id.name.encode() + invoice.partner_id.commercial_partner_id.ref.encode() + eposta.encode() + tutar.encode() + invoice.number.encode() + invoice.company_id.hash_code.encode()).hexdigest().upper(),
                    }
            invoice.altinkaya_payment_url = "?" + url_encode(params)

