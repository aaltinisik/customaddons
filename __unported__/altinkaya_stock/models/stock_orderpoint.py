# -*- encoding: utf-8 -*-
#
# Created on Jan 17, 2020
#
# @author: dogan
#
from odoo import models, fields, api


class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    # categ_id = fields.Many2one('product.category',
    #                            related='product_id.categ_id',
    #                            string='Category',
    #                            store=True, readonly=True)

    transfers_to_customer_ids = fields.Many2many(
        'stock.move',
        string='Transfers to Customers',
        compute='_compute_customer_transfers'
    )

    production_ids = fields.Many2many(
        'mrp.production',
        string='Manufacturing Orders',
        compute='_compute_productions'
    )

    done_purchaseline_ids = fields.Many2many(
        'purchase.order.line',
        string='Previous Purchases',
        compute='_compute_done_purchaselines'
    )

    done_orderline_ids = fields.Many2many(
        'sale.order.line',
        string='Done Orders',
        compute='_compute_done_orderlines'
    )

    @api.multi
    @api.depends('product_id')
    def _compute_productions(self):
        for wizard in self:
            wizard.production_ids = self.env['mrp.production'].search([('product_id', '=', wizard.product_id.id),
                                                                       ('state', 'not in', ['cancel'])],
                                                                      order='create_date desc')

    @api.multi
    @api.depends('product_id')
    def _compute_customer_transfers(self):
        for wizard in self:
            wizard.transfers_to_customer_ids = self.env['stock.move'].search([('product_id', '=', wizard.product_id.id),
                                                                              ('state', 'not in', ['draft', 'cancel'])],
                                                                             order='create_date desc')

    @api.multi
    @api.depends('product_id')
    def _compute_done_purchaselines(self):
        for wizard in self:
            wizard.done_purchaseline_ids = self.env['purchase.order.line'].search(
                [('product_id', '=', wizard.product_id.id),
                 ('state', 'not in', ['draft', 'cancel'])],
                limit=40, order='create_date desc')

    @api.multi
    @api.depends('product_id')
    def _compute_done_orderlines(self):
        for wizard in self:
            wizard.done_orderline_ids = self.env['sale.order.line'].search([('product_id', '=', wizard.product_id.id),
                                                                            ('state', 'not in', ['draft', 'cancel'])],
                                                                           order='create_date desc')
