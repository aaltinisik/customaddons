import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import clean_context


class ProductReplenish(models.TransientModel):
    _inherit = 'product.replenish'
    priority = fields.Selection([('0', 'Not urgent'), ('1', 'Normal'), ('2', 'Urgent'), ('3', 'Very Urgent')],
                                'Priority', default='1')

    @api.multi
    def launch_replenishment(self):
        uom_reference = self.product_id.uom_id
        self.quantity = self.product_uom_id._compute_quantity(self.quantity, uom_reference)
        try:
            self.env['procurement.group'].with_context(clean_context(self.env.context))._run(
                self.product_id,
                self.quantity,
                uom_reference,
                self.warehouse_id.lot_stock_id, # Location
                'INT:%s' % self.env.user.name.replace(' ', '.'), # Name
                'INT:%s' % self.env.user.name.replace(' ', '.'), # Origin
                self._prepare_run_values(), # Values
                self.priority, # Priority
            )
        except UserError as error:
            raise UserError(error)
