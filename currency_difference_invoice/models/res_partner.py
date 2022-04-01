# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.one
    def _compute_currency_difference_amls(self):
        difference_aml_domain = [('partner_id', '=', self.id),
                                 ('journal_id', '=', self.company_id.currency_exchange_journal_id.id),
                                 ('difference_checked', '=', False),
                                 ('full_reconcile_id', '!=', False)]

        difference_amls = self.env['account.move.line'].search(difference_aml_domain)
        if len(difference_amls) > 0:
            self.currency_difference_amls = difference_amls
        else:
            self.currency_difference_amls = False

    currency_difference_amls = fields.Many2many('account.move.line', string='Currency Difference Move Lines',
                                                compute='_compute_currency_difference_amls')
    currency_difference_checked = fields.Boolean(string='Currency Difference Checked', default=False)

    def unreconcile_partners_amls(self):
        if self.property_account_receivable_id.currency_id and self.property_account_payable_id.currency_id:
            reconciled_amls = self.env['account.move.line'].search([('partner_id', '=', self.id),
                                                                    ('full_reconcile_id', '!=', False)])
            if reconciled_amls:
                reconciled_amls.remove_move_reconcile()

    def calc_difference_invoice(self):
        if self.property_account_receivable_id.currency_id and self.property_account_payable_id.currency_id:
            inv_obj = self.env['account.invoice']
            diff_inv_journal = self.env['account.journal'].search([('code', '=', 'KFARK')], limit=1)
            draft_dif_inv = inv_obj.search([('state', '=', 'draft'),
                                            ('journal_id', '=', diff_inv_journal.id),
                                            ('partner_id', '=', self.id),
                                            ('currency_id', '=', self.env.user.company_id.currency_id.id)])
            if draft_dif_inv:
                for x in draft_dif_inv:
                    x.action_invoice_cancel()

            difference_aml_domain = [('partner_id', '=', self.id),
                                     ('journal_id', '=', self.company_id.currency_exchange_journal_id.id),
                                     ('difference_checked', '=', False),
                                     ('full_reconcile_id', '!=', False)]

            difference_amls = self.env['account.move.line'].search(difference_aml_domain)
            if difference_amls:
                inv_lines_to_create = []
                comment_einvoice = 'Aşağıdaki faturaların kur farkıdır:\n'
                for diff_aml in difference_amls:
                    inv_line_name = "Kur Farkı"
                    tax_18 = self.env['account.tax'].search(
                        [('type_tax_use', '=', 'sale'), ('amount', '=', 18.0), ('include_base_amount', '=', False)],
                        limit=1)
                    tax_8 = self.env['account.tax'].search(
                        [('type_tax_use', '=', 'sale'), ('amount', '=', 8.0), ('include_base_amount', '=', False)],
                        limit=1)
                    inv_ids = diff_aml.full_reconcile_id.reconciled_line_ids.filtered(lambda r: r.invoice_id).mapped(
                        'invoice_id')
                    if len(inv_ids) > 0:
                        kdv_18_taxes = sum(inv_ids.mapped('tax_line_ids').filtered(lambda r:
                                                                                   r.tax_id.amount == 18).mapped(
                            'amount'))

                        kdv_8_taxes = sum(inv_ids.mapped('tax_line_ids').filtered(lambda r:
                                                                                  r.tax_id.amount == 8).mapped(
                            'amount'))

                        rate_18 = round(100.0 * (kdv_18_taxes / 18.0) / sum(inv_ids.mapped('amount_untaxed')), 3)
                        rate_8 = round(100.0 * (kdv_8_taxes / 8.0) / sum(inv_ids.mapped('amount_untaxed')), 3)

                        comment_einvoice += ', '.join(inv_id.supplier_invoice_number
                                                      if inv_id.supplier_invoice_number
                                                      else inv_id.number
                                                      for inv_id in inv_ids)

                        if rate_18 > 0.001:
                            amount_untaxed = (diff_aml.debit or diff_aml.credit) * rate_18 / (1 + tax_18.amount / 100.0)
                            inv_lines_to_create.append({
                                'difference_base_aml_id': diff_aml.id,
                                'name': inv_line_name,
                                'uom_id': 1,
                                'account_id': self.env.user.company_id.currency_diff_inv_account_id.id,
                                'price_unit': amount_untaxed,
                                'invoice_line_tax_ids': [(6, False, [tax_18.id])]})

                        if rate_8 > 0.001:
                            amount_untaxed = (diff_aml.debit or diff_aml.credit) * rate_8 / (1 + tax_8.amount / 100.0)
                            inv_lines_to_create.append({
                                'difference_base_aml_id': diff_aml.id,
                                'name': inv_line_name,
                                'uom_id': 1,
                                'account_id': self.env.user.company_id.currency_diff_inv_account_id.id,
                                'price_unit': amount_untaxed,
                                'invoice_line_tax_ids': [(6, False, [tax_8.id])]})
                    else:
                        comment_einvoice = ''
                        amount_untaxed = (diff_aml.debit or diff_aml.credit) / (1 + tax_18.amount / 100.0)
                        inv_lines_to_create.append({
                            'difference_base_aml_id': diff_aml.id,
                            'name': inv_line_name,
                            'uom_id': 1,
                            'account_id': self.env.user.company_id.currency_diff_inv_account_id.id,
                            'price_unit': amount_untaxed,
                            'invoice_line_tax_ids': [(6, False, [tax_18.id])]})

                    diff_aml.write({'difference_checked': True})

                if inv_lines_to_create:
                    if sum(x['price_unit'] for x in inv_lines_to_create) < 0.0:
                        # [x.update({'price_unit': -x['price_unit']}) for x in inv_lines_to_create]
                        inv_type = 'out_refund'
                    else:
                        inv_type = 'out_invoice'

                    created_inv_lines = self.env['account.invoice.line'].create(inv_lines_to_create)
                    dif_inv = inv_obj.create({'partner_id': self.id,
                                              'journal_id': diff_inv_journal.id,
                                              'currency_id': self.env.user.company_id.currency_id.id,
                                              'type': inv_type,
                                              'comment_einvoice': comment_einvoice})

                    dif_inv.invoice_line_ids = [(6, False, [x.id for x in created_inv_lines])]
                    dif_inv._onchange_invoice_line_ids()
                    return dif_inv

        return False

    @api.multi
    def action_generate_currency_diff_invoice(self):

        self.ensure_one()
        invoice = self.calc_difference_invoice()

        if not invoice:
            raise UserError(_('No invoice created!'))

        if invoice.type == "out_invoice":
            action = self.env.ref("account.action_invoice_tree1")
        elif invoice.type == "out_refund":
            action = self.env.ref("account.action_invoice_out_refund")

        if action:
            action_dict = action.read()[0]
            form_view = [(self.env.ref('account.invoice_form').id, 'form')]
            if 'views' in action_dict:
                action_dict['views'] = form_view + [
                    (state, view) for state, view in action[
                        'views'] if view != 'form']
            else:
                action_dict['views'] = form_view
            action_dict['res_id'] = invoice.id

            return action_dict

        return False
