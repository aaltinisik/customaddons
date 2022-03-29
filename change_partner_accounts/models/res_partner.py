# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def change_accounts(self):
        view = self.env.ref('change_partner_accounts.view_change_partner_accounts')
        return {
            'name': _('Change Partner Accounts'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'change.partner.accounts',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': self.env.context,
        }
