# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from openerp import models, fields, api, _
from openerp.exceptions import Warning

from datetime import datetime

class partner_account_wizard(models.TransientModel):
    _name = 'partner.account.wizard'

    agree = fields.Boolean(string="Do you want to Update Accounts")

    @api.multi
    def update_accounts(self):
        if not self.agree:
            raise Warning("Please select the checkbox")
        partner_ids = self.env['res.partner'].browse(self._context.get('active_ids'))
        account_ids_lst = []
        for partner_id in partner_ids:

            if partner_id.property_account_receivable.id not in [31640, 15888]:
                if partner_id.ref and partner_id.country_id.code:
                    z_receivable_export = False
                    z_payable_export = False
                    code_prefix = "Y"
                    if partner_id.country_id.code != 'TR':
                        z_receivable_export = '120.' + code_prefix + (
                            partner_id.ref and str(partner_id.ref).strip() or '')
                        z_payable_export = '320.' + code_prefix + (partner_id.ref and partner_id.ref.strip() or '')
                    else:
                        z_receivable_export = '120.' + (partner_id.ref and str(partner_id.ref).strip() or '')
                        z_payable_export = '320.' + (partner_id.ref and str(partner_id.ref).strip() or '')
                    partner_id.write({'z_receivable_export': z_receivable_export,
                                 'z_payable_export': z_payable_export})


            if partner_id.property_account_receivable.id not in [31638,31640,15888]:

                if partner_id.property_account_receivable.id != 31638 and \
                        partner_id.property_account_receivable.id:
                    if partner_id.property_account_receivable.id not in [53, 12007,8,13,25]:
                        account_ids_lst.append(partner_id.property_account_receivable.id)
                    self._cr.execute('''update account_voucher_line set account_id=31638
                                             where account_id=%s
                                         ''' % (partner_id.property_account_receivable.id))
                    self._cr.execute('''update account_move_line set account_id=31638
                                             where account_id=%s
                                         ''' % (partner_id.property_account_receivable.id))
                    self._cr.execute('''update account_invoice set account_id=31638
                                             where account_id=%s
                                         ''' % (partner_id.property_account_receivable.id))

                if partner_id.property_account_payable.id not in [31639] and \
                        partner_id.property_account_payable.id:
                    if partner_id.property_account_receivable.id not in [53, 12007,8,13,25]:
                        account_ids_lst.append(partner_id.property_account_payable.id)
                    self._cr.execute('''update account_voucher_line set account_id=31639
                                             where account_id=%s
                                         ''' % (partner_id.property_account_payable.id))
                    self._cr.execute('''update account_move_line set account_id=31639
                                         where account_id=%s
                                         ''' % (partner_id.property_account_payable.id))
                    self._cr.execute('''update account_invoice set account_id=31639
                                             where account_id=%s
                                         ''' % (partner_id.property_account_payable.id))
                if account_ids_lst:
                    self._cr.execute('''delete from account_account where id in %s
                    ''' % (" (%s) " % ','.join(map(str, account_ids_lst))))
                    account_ids_lst=[]

                partner_id.write({'property_account_receivable': 31638,
                                  'property_account_payable': 31639})

        return True

class account_merge_wizard(models.TransientModel):
    _name = 'account.merge.wizard'

    agree = fields.Boolean(string="Do you want to Update Accounts")

    @api.multi
    def merge_accounts(self):
        if not self.agree:
            raise Warning("Please select the checkbox")
        account_ids = self.env['account.account'].browse(self._context.get('active_ids'))
        account_ids_lst = []
        for account_id in account_ids:

            if account_id.parent_id.id in [8]:
                self._cr.execute('''update account_voucher_line set account_id=31638
                                         where account_id=%s
                                     ''' % (account_id.id))
                self._cr.execute('''update account_move_line set account_id=31638
                                         where account_id=%s
                                     ''' % (account_id.id))
                self._cr.execute('''update account_invoice set account_id=31638
                                         where account_id=%s
                                     ''' % (account_id.id))
                if account_id.id not in [31638,31639]:
                    account_ids_lst.append(account_id.id)

            if account_id.parent_id.id in [13]:
                self._cr.execute('''update account_voucher_line set account_id=31639
                                         where account_id=%s
                                     ''' % (account_id.id))
                self._cr.execute('''update account_move_line set account_id=31639
                                         where account_id=%s
                                     ''' % (account_id.id))
                self._cr.execute('''update account_invoice set account_id=31639
                                         where account_id=%s
                                     ''' % (account_id.id))
                if account_id.id not in [31638,31639]:
                    account_ids_lst.append(account_id.id)

            if account_ids_lst:
                self._cr.execute('''delete from account_account where id in %s
                ''' % (" (%s) " % ','.join(map(str, account_ids_lst))))
                account_ids_lst = []

        return True

#     @api.multi
#     def create_payments(self):
#         if not self.agree:
#             raise Warning("Please select the checkbox")
#         voucher_obj = self.env['account.voucher']
#         default_data = ["comment", "line_cr_ids", "is_multi_currency", "paid_amount_in_company_currency",
#                           "line_dr_ids", "journal_id", "currency_id", "narration", "partner_id",
#                           "payment_rate_currency_id", "reference", "writeoff_acc_id", "state", "pre_line",
#                             "payment_option", "account_id", "company_id", "period_id", "date", "payment_rate"]
#         journal_id = self.env['account.journal'].search([('type', '=', 'cash')], limit=1)
#         voucher_default_values = voucher_obj.default_get(default_data)
#         for invoice in self.env['account.invoice'].browse(self._context.get('active_ids')):
#             if invoice.state == 'open':
#                 voucher_values = {}
#                 vouchar_lines = []
#                 voucher_values.update({'partner_id':invoice.partner_id.id,
#                                        'amount':invoice.amount_total,
#                                        'type':'receipt',
#                                        'account_id':journal_id.default_credit_account_id.id,
#                                        'journal_id':journal_id.id,
#                                        'name':invoice.number,
#                                        'period_id':voucher_default_values.get('period_id'),
#                                        'company_id':voucher_default_values.get('company_id'),
#                                        'state':'draft',
#                                        'date':voucher_default_values.get('date'),
#                                        'payment_rate':voucher_default_values.get('payment_rate')})
#                 for line in invoice.move_id.line_id:
#                     if line.debit:
#                         vouchar_lines.append((0, False, {'move_line_id':line.id,
#                                                          'amount':line.debit,
#                                                          'account_id':line.account_id.id,
#                                                          'date_original':line.date,
#                                                          'date_due':line.date_maturity,
#                                                          'amount_original':line.debit or line.credit or 0.0,
#                                                          'amount_unreconciled': abs(line.amount_residual_currency),
#                                                      }))
#                 if vouchar_lines:
#                     voucher_values.update({'line_dr_ids': [], 'line_cr_ids':vouchar_lines})
#                     voucher_id = voucher_obj.create(voucher_values)
#                     print "\n-------------voucher_id", voucher_id
#                     if voucher_id:
#                         voucher_id.button_proforma_voucher()
#         return True

#     @api.multi
#     def create_accounts(self):
#         if not self.agree:
#             raise Warning("Please select the checkbox")
#         account_obj = self.env['account.account']
#         aat_obj = self.env['account.account.type']
#         imd_obj = self.env['ir.model.data']
#         receivable_type = aat_obj.search([('code', '=', 'receivable')], limit=1)
#         payable_type = aat_obj.search([('code', '=', 'payable')], limit=1)
#         for partner in self.env['res.partner'].browse(self._context.get('active_ids')):
#             if not partner.ref:
#                 raise Warning(_("You must define reference for creating accounts!"))
#             code_prefix = ""
#             turkey_code = u"TR"
#             if partner.parent_id:
#                 if partner.parent_id.country_id.code != turkey_code:
#                     code_prefix = "Y"
#             if partner.country_id.code != turkey_code:
#                 code_prefix = "Y"
#             code = '120.' + code_prefix + (partner.ref and str(partner.ref).strip() or '')
#             code_pay = '320.' + code_prefix + (partner.ref and str(partner.ref).strip() or '')
#             acc_receivable_id = account_obj.search([('code', '=', code)])
#             acc_payable_id = account_obj.search([('code', '=', code_pay)])
#             if acc_receivable_id:
#                 raise Warning(_("Account Receivable is already created with this reference."))
#             if acc_payable_id:
#                 raise Warning(_("Account Payable is already created with this reference."))
#             parent_rec_id = imd_obj.get_object_reference('account', 'conf_a_recv')[1]
#             parent_cre_id = imd_obj.get_object_reference('account', 'conf_a_pay')[1]
#             acc_rec_data = {'code': code,
#                             'name': partner.name,
#                             'parent_id': parent_rec_id,
#                             'reconcile':True,
#                             'type':'receivable',
#                             'user_type': receivable_type and receivable_type.id or False }
#             acc_recievable = account_obj.create(acc_rec_data)
#             acc_pay_data = {'code': code_pay,
#                             'name': partner.name,
#                             'parent_id': parent_cre_id,
#                             'reconcile':True,
#                             'type':'payable',
#                             'user_type': payable_type and payable_type.id or False }
#             acc_payable = account_obj.create(acc_pay_data)
#             partner.write({'property_account_receivable': acc_recievable.id,
#                            'property_account_payable': acc_payable.id})
#         return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
