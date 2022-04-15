from openerp import models, fields



class stock_location(models.Model):
    _inherit = 'stock.location'

    priority = fields.Integer('Removal Priority', help='high priority locations will be reserved first', default=10)
