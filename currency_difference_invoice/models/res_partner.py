# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.tools import float_is_zero, float_compare

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    has_secondary_curr = fields.Boolean(string='Has secondary currency?', default=False)
    secondary_curr_id = fields.Many2one('res.currency', string='Currency')

    def calc_difference_invoice(self):
        prec = self.env['decimal.precision'].precision_get('Account')
        if self.has_secondary_curr:

            invoices_domain = [('partner_id', '=', self.id), ('journal_id.type', 'in', ['sale']),
                               ('currency_difference_checked', '=', False),
                               ('account_id', 'in', [self.property_account_receivable_id.id,
                                                     self.property_account_payable_id.id])]

            payments_domain = [('partner_id', '=', self.id), ('journal_id.type', 'in', ['bank', 'cash']),
                               ('currency_difference_checked', '=', False),
                               ('account_id', 'in', [self.property_account_receivable_id.id,
                                                     self.property_account_payable_id.id]),
                               ('credit', '>', 0.0)]

            line_obj = self.env['account.move.line']
            difference_inv = self.env['account.invoice'].create({'name': 'Difference',
                                                                 'partner_id': self.id,
                                                                 'journal_id': 4,
                                                                 'currency_id': self.company_id.currency_id.id})
            payments = line_obj.search(payments_domain)
            lines_to_create = []
            onhand_credit = 0.0 # elimizdeki ödeme miktarı TL

            next_index = -1
            for invoice in line_obj.search(invoices_domain):
                total = invoice.debit - onhand_credit
                # total faturanın kalan ödenecek miktarı
                if not float_compare(total, 0.0, precision_digits=prec) is -1 or 0:
                    for index, payment in enumerate(payments[next_index + 1:]):
                        amount_currency = round(payment.amount_currency or payment._calculate_amount_currency(), prec)
                        #amount_currency ödemenin döviz cinsinden miktarı
                        onhand_credit = self.secondary_curr_id._convert(amount_currency, payment.company_id.currency_id,
                                                                        payment.company_id, payment.date, round=False)
                        #onhand_credit ödemenin ödeme tarihindeki TL cinsinden miktarı
                        if float_compare(onhand_credit, total, precision_digits=prec) >= 0:
                            next_index += index+1
                            break

                onhand_credit -= invoice.debit
                if onhand_credit < -0.1:
                    invoice.currency_difference_amount = onhand_credit
                    lines_to_create.append({
                        'invoice_id': difference_inv.id,
                        'name': f'{invoice.invoice_id.name} Invoice Currency Difference',
                        'account_id': 279,
                        'quantity': 1,
                        'price_unit': abs(onhand_credit),
                    })
                    onhand_credit = 0.0

            if lines_to_create:
                created_inv_lines = self.env['account.invoice.line'].create(lines_to_create)
                difference_inv.invoice_line_ids = [(6, False, [x.id for x in created_inv_lines])]



            # for line in lines:
            #     payment = line.credit or line.debit
            #     amount_currency = round(abs(line.amount_currency or line._calculate_amount_currency()), prec)
