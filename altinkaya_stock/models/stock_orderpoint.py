# -*- encoding: utf-8 -*-
#
#Created on Jan 17, 2020
#
#@author: dogan
#
from odoo import models, fields, api

class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    categ_id = fields.Many2one('product.category',
                                 related='product_id.categ_id',
                                 string='Category',
                                 store=True, readonly=True)

