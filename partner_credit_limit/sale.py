#-*- coding:utf-8 -*-
from openerp import models, api, _
from openerp.exceptions import Warning


class sale_order(models.Model):
    _inherit = "sale.order"

    @api.one
    def action_wait(self):
        self.check_limit()
        return super(sale_order, self).action_wait()

    @api.one
    def check_limit(self):

        def convert_to_company_currency_amount(currency_id, amount):
            if currency_id.id == self.company_id.currency_id.id:
                return amount
            else:
                company_curr_amount = currency_id.compute(amount, self.company_id.currency_id)
                return company_curr_amount
            
            
        if self.order_policy == 'prepaid':
            return True
        
        commercial_partner_id = self.partner_id.commercial_partner_id
        
        if commercial_partner_id.credit_limit == 0.0:
            return True

        order_amount = convert_to_company_currency_amount(self.currency_id, self.amount_total)
        
        
        # We sum from all the sale orders that are aproved, the sale order
        # lines that are not yet invoiced
        domain = [('order_id.partner_id', 'child_of', commercial_partner_id.id),
                  ('invoiced', '=', False),
                  ('order_id.state', 'not in', ['draft', 'cancel', 'sent'])]
        order_lines = self.env['sale.order.line'].search(domain)
        none_invoiced_amount = sum([convert_to_company_currency_amount(x.order_id.currency_id, x.price_subtotal) for x in order_lines])

        # We sum from all the invoices that are in draft the total amount
        domain = [
            ('partner_id', 'child_of', commercial_partner_id.id), ('state', '=', 'draft')]
        draft_invoices = self.env['account.invoice'].search(domain)
        draft_invoices_amount = sum([convert_to_company_currency_amount(x.currency_id, x.amount_total) for x in draft_invoices])

        
        available_credit = commercial_partner_id.credit_limit - \
            commercial_partner_id.credit - \
            none_invoiced_amount - draft_invoices_amount + commercial_partner_id.debit

        if order_amount > available_credit:
            raise Warning(_('Insufficent partner credit limit!'))
            return False
        return True
