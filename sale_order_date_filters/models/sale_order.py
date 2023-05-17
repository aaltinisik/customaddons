from odoo import models, api

class SaleOrderInherit(models.Model):
    _inherit = "sale.order"
