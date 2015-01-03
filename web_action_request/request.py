# -*- coding: utf-8 -*-

from openerp.osv import osv


class ActionRequest(osv.AbstractModel):
    _name = 'action.request'
    _description = 'Action Request'
    _inherit = [
        'postgres.notification',
    ]
    _postgres_channel = 'action.request'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
