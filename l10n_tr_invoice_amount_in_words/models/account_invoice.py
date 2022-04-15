# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015, Eska Yazılım ve Danışmanlık A.Ş.
#    http://www.eskayazilim.com.tr
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    
    
    
    @api.one
    @api.depends('amount_total','currency_id')
    def _compute_invoice_amount_in_words(self):
        lang = self.env.context.get('lang', self.sudo().company_id.partner_id.lang)
        self.invoice_amount_in_words = self.currency_id.with_context({'lang': lang}).amount_to_text(
            self.amount_total)


    invoice_amount_in_words = fields.Char(compute='_compute_invoice_amount_in_words',
                                 string='Amount to Text')

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
    @api.one
    @api.depends('amount_total','currency_id')
    def _compute_sale_order_amount_in_words(self):
        lang = self.env.context.get('lang', self.sudo().company_id.partner_id.lang)
        self.sale_order_amount_in_words = self.currency_id.with_context({'lang': lang}).amount_to_text(
            self.amount_total)


    sale_order_amount_in_words = fields.Char(compute='_compute_sale_order_amount_in_words',
                                 string='Amount to Text')
    
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    
    @api.one
    @api.depends('amount_total','currency_id')
    def _compute_purchase_order_amount_in_words(self):
        lang = self.env.context.get('lang', self.sudo().company_id.partner_id.lang)
        self.purchase_order_amount_in_words = self.currency_id.with_context({'lang': lang}).amount_to_text(
            self.amount_total)


    purchase_order_amount_in_words = fields.Char(compute='_compute_purchase_order_amount_in_words',
                                 string='Amount to Text')
    
class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    
    @api.one
    @api.depends('amount','currency_id')
    def _compute_account_payment_amount_in_words(self):
        lang = self.env.context.get('lang', self.sudo().company_id.partner_id.lang)
        self.account_payment_amount_in_words = self.currency_id.with_context({'lang': lang}).amount_to_text(
            self.amount)


    account_payment_amount_in_words = fields.Char(compute='_compute_account_payment_amount_in_words',
                                 string='Amount to Text')

