from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ChangePartnerAccounts(models.TransientModel):
    _name = 'change.partner.accounts'

    account_receivable_id = fields.Many2one('account.account', string='Account Receivable', required=True)
    account_payable_id = fields.Many2one('account.account', string='Account Payable', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)

    @api.model
    def default_get(self, field_list):
        res = super(ChangePartnerAccounts, self).default_get(field_list)
        if self.env.context.get('active_model') == 'res.partner':
            res['partner_id'] = self.env.context.get('active_id')
        return res

    @api.one
    def change_accounts(self):
        if self.account_payable_id.currency_id != self.account_receivable_id.currency_id:
            raise UserError(_('Accounts must be in the same currency'))

        old_receivable_id = self.partner_id.property_account_receivable_id.id
        old_payable_id = self.partner_id.property_account_payable_id.id

        if (old_payable_id == self.account_payable_id.id) or (old_receivable_id == self.account_receivable_id.id):
            raise UserError(_('Accounts must be different than the current ones'))

        cr = self.env.cr
        cr.execute("""update account_move_line line set account_id = t.new_account_id
                    from (select ml.id as line_id, ml.account_id, ml.partner_id,           
                    case
                    when ml.account_id = {0} then {1} --- receivable
                    when ml.account_id = {2} then {3} --- payable
                    else ml.account_id
                    end as new_account_id
            
                    from account_move_line as ml 
                    where ml.partner_id = {4})
                    t where t.line_id = line.id""".format(old_receivable_id,
                                                          self.account_receivable_id.id,
                                                          old_payable_id,
                                                          self.account_payable_id.id,
                                                          self.partner_id.id))

        self.partner_id.write({'property_account_receivable_id': self.account_receivable_id.id,
                               'property_account_payable_id': self.account_payable_id.id})

        self.calculate_amount_currency_on_partner_amls()
        return {"type": "ir.actions.act_window_close"}

    @api.one
    def calculate_amount_currency_on_partner_amls(self):
        cr = self.env.cr
        company_currency = self.env.user.company_id.currency_id
        currency_id = (self.partner_id.property_account_receivable_id.currency_id and
                       self.partner_id.property_account_receivable_id.currency_id) or \
                      False

        partner_amls = self.env['account.move.line'].search([('partner_id', '=', self.partner_id.id),
                                                             ('account_id', 'in',
                                                              [self.partner_id.property_account_receivable_id.id,
                                                               self.partner_id.property_account_payable_id.id]),
                                                             ('currency_id', '=', False)])

        for aml in partner_amls:
            amount_currency = company_currency._convert(aml.debit - aml.credit,
                                                        currency_id,
                                                        self.env.user.company_id, aml.date)

            amount_residual_currency = company_currency._convert(aml.amount_residual,
                                                                 currency_id,
                                                                 self.env.user.company_id, aml.date)

            cr.execute(
                """ update account_move_line
                
                 set
                  amount_currency = {0},
                  currency_id = {1},
                  amount_residual_currency = {2}
                
                where id = {3}""".format(amount_currency,
                                         currency_id.id,
                                         amount_residual_currency,
                                         aml.id))

        cr.commit()
