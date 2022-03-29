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
        cr = self.env.cr
        cr.execute("""update account_move_line line set account_id = t.account_id
                    from (select ml.id as line_id, ml.account_id, ml.partner_id,           
                    case
                    when ml.account_id = {0} then {1} --- receivable
                    when ml.account_id = {2} then {3} --- payable
                    else ml.account_id
                    end as account_id
            
                    from account_move_line as ml 
                    where ml.partner_id = {4})
                    t where t.line_id = line.id""".format(old_receivable_id,
                                                          self.account_receivable_id.id,
                                                          old_payable_id,
                                                          self.account_payable_id.id,
                                                          self.partner_id.id))

        self.partner_id.write(value={'property_account_receivable_id': self.account_receivable_id.id,
                                     'property_account_payable_id': self.account_payable_id.id})

        # 3. account.move.line'larda amount_currencysi olmayan veya yeni hesaba uymayanları düzelteceğiz
        return {"type": "ir.actions.act_window_close"}
