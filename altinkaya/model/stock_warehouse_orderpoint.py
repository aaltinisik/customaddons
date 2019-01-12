# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    categ_id = fields.Many2one('product.category',
                                 related='product_id.categ_id',
                                 string='Category',
                                 store=True, readonly=True)
