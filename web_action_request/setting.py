# -*- coding: utf-8 -*-

from openerp.osv import osv, fields


class Setting(osv.TransientModel):
    _name = 'web.action.request.setting'
    _description = 'test the request'
    _inherit = 'res.config.settings'

    _columns = {
        'action_id': fields.many2one('ir.actions.act_window', 'Act Window', required=True),
    }

    def button_check_action_request(self, cr, uid, ids, context=None):
        r = self.read(cr, uid, ids[0], ['action_id'], load="_classic_write",
                      context=context)
        action = self.pool.get('ir.actions.act_window').read(
            cr, uid, r['action_id'], [], context=context)

        self.pool.get('action.request').notify(
            cr, uid, to_id=uid, **action)
        return True
