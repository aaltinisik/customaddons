# -*- encoding: utf-8 -*-

from openerp.osv import osv, fields


class res_partner(osv.Model):
    _inherit = 'res.partner'
    _columns = {
    'has_secondary_curr': fields.boolean(u'Dövizle çalışıyor', default=False),
    'secondary_curr_id': fields.many2one('res.currency', string=u'Döviz birimi')
    }

    def action_print_dovizli_statement(self, cr, uid, ids, context=None):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'wizard.partner.doviz.statement',
            'target': 'new'
         }

res_partner()