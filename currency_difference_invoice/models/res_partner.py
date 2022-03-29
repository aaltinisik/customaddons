# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    has_secondary_curr = fields.Boolean(string='Has secondary currency?', default=False)
    secondary_curr_id = fields.Many2one('res.currency', string='Currency')

    def unreconcile_partners_amls(self):
        if self.has_secondary_curr:
            reconciled_amls_domain = [('partner_id', '=', self.id),
                                      ('full_reconcile_id', '!=', False)]

            reconciled_amls = self.env['account.move.line'].search(reconciled_amls_domain)
            aml_to_unreconcile = self.env['account.move.line']
            if reconciled_amls:
                for reconcile_obj in [aml.full_reconcile_id for aml in reconciled_amls]:
                    aml_to_unreconcile |= reconcile_obj.reconciled_line_ids

                aml_to_unreconcile.remove_move_reconcile()

    def calc_difference_invoice(self):
        if self.has_secondary_curr:
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
                for diff_aml in difference_amls:
                    inv_line_name = f"Kur Farkı / {diff_aml.payment_id.move_name} /" \
                                    f" {diff_aml.invoice_id.display_name} {diff_aml.date.strftime('%d.%m.%Y')}"
                    aml_tax = fields.first(diff_aml.invoice_id.tax_line_ids).tax_id
                    amount = diff_aml.debit or diff_aml.credit
                    if aml_tax and aml_tax.amount_type == 'percent':
                        amount = (amount / (100.0 + aml_tax.amount)) * 100.0

                    inv_lines_to_create.append({
                        'difference_base_aml_id': diff_aml.id,
                        'name': inv_line_name,
                        'uom_id': 1,
                        'account_id': self.env.user.company_id.currency_diff_inv_account_id.id,
                        'price_unit': amount,
                        'invoice_line_tax_ids': [
                            (6, False, [aml_tax.id] if aml_tax else [self.env['account.tax'].search(
                                [('type_tax_use', '=', 'sale'), ('amount', '=', 0.0)], limit=1).id])],
                    })
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
                                              'type': inv_type})

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

