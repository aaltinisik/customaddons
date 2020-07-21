
from odoo import models, fields


class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    selectable_on_procurement_wizard = fields.Boolean('Selectable on procurement wizard')

