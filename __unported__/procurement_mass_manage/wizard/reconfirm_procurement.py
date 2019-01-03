# -*- coding: utf-8 -*-

import logging
from openerp import models, fields, api, _
_logger = logging.getLogger(__name__)

class reconfirm_procurement(models.TransientModel):
    _name = 'procurement.reconfirm.wiz'
    _description = 'ReConfirm Procurement'

    @api.multi
    def reconfirm_procurement(self):
        context = dict(self.env.context)
        if context.get('active_ids') and context.get('active_model') == 'procurement.order':
            active_ids = self.env['procurement.order'].browse(context.get('active_ids'))
            for procurement in active_ids:
                if procurement.state == 'cancel':
                    procurement.reset_to_confirmed()
                else:
                    _logger.info('%s procurement id in %s state so it is skipped' %(str(procurement.id),procurement.state))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
