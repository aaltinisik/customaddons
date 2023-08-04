from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    priority = fields.Integer(related='location_id.priority', help='high priority quants will be reserved first',
                             readonly=True, store=True)

    @api.model
    def _get_removal_strategy_order(self, removal_strategy):
        if removal_strategy == 'priorityfifo':
            return 'priority, in_date ASC NULLS FIRST, id'
        return super(StockQuant, self)._get_removal_strategy_order(removal_strategy)
