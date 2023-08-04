import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import clean_context


class ProductReplenish(models.TransientModel):
    _inherit = 'product.replenish'
    priority = fields.Selection([('0', 'Acil Değil'), ('1', 'Normal'), ('2', 'Acil'), ('3', 'Çok Acil')],
                                'Öncelik', default='1')

    @api.multi
    def launch_replenishment(self):
        uom_reference = self.product_id.uom_id
        self.quantity = self.product_uom_id._compute_quantity(self.quantity, uom_reference)
        values = self._prepare_run_values()
        try:
            self.env['procurement.group'].with_context(clean_context(self.env.context))._run(
                self.product_id,
                self.quantity,
                uom_reference,
                self.warehouse_id.lot_stock_id, # Location
                'INT:%s' % self.env.user.name.replace(' ', '.'), # Name
                'INT:%s' % self.env.user.name.replace(' ', '.'), # Origin
                values, # Values
                self.priority, # Priority
            )
        except UserError as error:
            raise UserError(error)
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'procurement.group',
            'res_id': values['group_id'].id,
            'type': 'ir.actions.act_window',
        }