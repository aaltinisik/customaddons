from odoo import models, api, _
from odoo.exceptions import UserError


class ChangePartnerAccountsUSD(models.TransientModel):
    _name = 'change.partner.accounts.usd'
    _description = "Changing partner accounts to USD Wizard"

    @api.multi
    def change_partners_account_to_usd(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        partners = self.env['res.partner'].browse(active_ids)
        errors = []
        for record in self.web_progress_iter(partners, msg="Müşterilerin hesapları değiştiriliyor..."):
            try:
                record.change_accounts_to_usd()
                record._get_partner_currency()
                self.env.cr.commit()
            except:
                errors.append(record.display_name)
        if len(errors) > 0:
            raise UserError(_("Action is completed but there is an error happened for these partners\n %s" %
                            "\n".join(x for x in errors)))
        else:
            return {'type': 'ir.actions.act_window_close'}
