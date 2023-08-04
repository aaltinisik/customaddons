from odoo import api, models, fields, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class ProcurementGroup(models.Model):
    _inherit = "procurement.group"


    @api.model
    def _run(self, product_id, product_qty, product_uom, location_id, name, origin, values, priority):
        values.setdefault('company_id', location_id.company_id)
        values.setdefault('priority', priority)
        values.setdefault('date_planned', fields.Datetime.now())
        rule = self._get_rule(product_id, location_id, values)
        if not rule:
            raise UserError(_('No procurement rule found in location "%s" for product "%s".\n Check routes configuration.') % (location_id.display_name, product_id.display_name))
        action = 'pull' if rule.action == 'pull_push' else rule.action
        if hasattr(rule, '_run_%s' % action):
            getattr(rule, '_run_%s' % action)(product_id, product_qty, product_uom, location_id, name, origin, values)
        else:
            _logger.error("The method _run_%s doesn't exist on the procument rules" % action)
        return
