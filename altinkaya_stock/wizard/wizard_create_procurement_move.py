# -*- coding: utf-8 -*-
#
#Created on Oct 12, 2018
#
#@author: dogan
#

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_compare


# class CreateProcurementMoveLocation(models.TransientModel):
#     _name = 'create.procurement.move.location'
#     _description = 'Create procurement move location'
#
#     wizard_id = fields.Many2one('create.procurement.move', 'Wizard')
#     qty_to_procurement = fields.Float('Quantity to Procurement')
#     warehouse_id = fields.Many2one('stock.warehouse', string='Depo')
#     warehouse_id_readonly = fields.Many2one(related='warehouse_id', string='Depo')
#     qty_available = fields.Float('Mevcut', compute='_compute_qty')
#     qty_incoming = fields.Float('Gelen', compute='_compute_qty')
#     qty_outgoing = fields.Float('Giden', compute='_compute_qty')
#     qty_virtual = fields.Float('Tahmini', compute='_compute_qty')
#
#
#     @api.multi
#     @api.depends('wizard_id', 'warehouse_id')
#     def _compute_qty(self):
#         for record in self:
#             product = record.wizard_id.product_id
#             warehouse = record.warehouse_id
#             if product and warehouse:
#                 record.qty_available = product.with_context({'warehouse': warehouse.id}).qty_available
#                 record.qty_incoming = product.with_context({'warehouse': warehouse.id}).incoming_qty
#                 record.qty_outgoing = product.with_context({'warehouse': warehouse.id}).outgoing_qty
#                 record.qty_virtual = product.with_context({'warehouse': warehouse.id}).virtual_available
#             else:
#                 record.qty_available = 0.0
#                 record.qty_incoming = 0.0
#                 record.qty_outgoing = 0.0
#                 record.qty_virtual = 0.0


class CreateProcurementMove(models.TransientModel):
    _name = 'create.procurement.move'
    _description = 'Create procurement move'
        
    move_id = fields.Many2one('stock.move','Move', readonly=True)
    product_id = fields.Many2one('product.product',string='Product', related='move_id.product_id', readonly=True)
    
    move_qty = fields.Float('Demand Quantity', related='move_id.product_uom_qty', readonly=True)
    procure_move = fields.Boolean('Tedarik bu harekete mi oluşturulsun',default=True)
    uom = fields.Many2one('uom.uom', string='UoM', related='move_id.product_uom', readonly=True)

    # procurement_qty_ids = fields.One2many('create.procurement.move.location', 'wizard_id', string='Quantities')

    priority = fields.Selection([('0', 'Acil Değil'), ('1', 'Normal'), ('2', 'Acil'), ('3', 'Çok Acil')],
                                'Öncelik', default='1')

    qty_to_sincan = fields.Float('Tedarik')
    qty_to_merkez = fields.Float('Tedarik')
    qty_available_merkez = fields.Float('Mevcut', related='product_id.qty_available_merkez')
    qty_available_sincan = fields.Float('Mevcut', related='product_id.qty_available_sincan')
    qty_incoming_merkez = fields.Float('Gelen', related='product_id.qty_incoming_merkez')
    qty_incoming_sincan = fields.Float('Gelen', related='product_id.qty_incoming_sincan')
    qty_outgoing_merkez = fields.Float('Giden', related='product_id.qty_outgoing_merkez')
    qty_outgoing_sincan = fields.Float('Giden', related='product_id.qty_outgoing_sincan')
    qty_virtual_merkez = fields.Float('Tahmini', related='product_id.qty_virtual_merkez')
    qty_virtual_sincan = fields.Float('Tahmini', related='product_id.qty_virtual_sincan')

    production_ids = fields.Many2many('mrp.production',string='Manufacturing Orders', compute='_compute_productions')
    transfers_to_customer_ids = fields.Many2many('stock.move',string='Transfers to Customers',
                                                 compute='_compute_customer_transfers')
    pending_orderline_ids = fields.Many2many('sale.order.line', string='Pending Orders',
                                             compute='_compute_pending_orderlines')

    sale_qty30days = fields.Float(u'Son 1 ayda satılan', related='move_id.product_id.sale_qty30days', readonly=True, store=False)
    sale_qty180days = fields.Float(u'Son 6 ayda satılan', related='move_id.product_id.sale_qty180days', readonly=True, store=False)
    sale_qty360days = fields.Float(u'Son 1 senede satılan', related='move_id.product_id.sale_qty360days', readonly=True, store=False)

    @api.multi
    @api.depends('product_id')
    def _compute_productions(self):
        for wizard in self:
            wizard.production_ids = self.env['mrp.production'].search([('product_id','=',wizard.product_id.id),('state','not in', ['done','cancel'])],limit=40,order='create_date desc')

    @api.multi
    @api.depends('product_id')
    def _compute_customer_transfers(self):
        for wizard in self:
            wizard.transfers_to_customer_ids = self.env['stock.move'].search([('product_id','=',wizard.product_id.id),('state','not in', ['draft','done','cancel'])],limit=40,order='create_date desc')

    @api.multi
    @api.depends('product_id')
    def _compute_pending_orderlines(self):
        for wizard in self:
            wizard.pending_orderline_ids = self.env['sale.order.line'].search([('product_id','=',wizard.product_id.id),('state','not in', ['draft','done','cancel'])],limit=40,order='create_date desc')


    @api.onchange('move_id')
    def onchange_move_id(self):
        self.qty = self.move_id.remaining_qty
        
    
    @api.multi
    def action_create(self):
        self.ensure_one()
        if self.qty_to_sincan or self.qty_to_merkez:
            if self.procure_move:
                self.move_id._do_unreserve()
                self.move_id.procure_method = 'make_to_order'
                self.move_id.write({'state': 'waiting'})

            if self.qty_to_sincan > 0.0:
                self.create_procurement_sincan()
            if self.qty_to_merkez > 0.0:
                self.create_procurement_merkez()
        else:
            raise UserError(_(
                "Tedarik icin miktar belirtmediniz."))

    @api.multi
    def create_procurement_sincan(self):
        self.ensure_one()
        warehouse = self.env['stock.warehouse'].search([('id', '=', 2)])
        group_id = self.env["procurement.group"].create({
            'name': u"%s" % (warehouse.name) + " Açan: " + self.env.user.name,
        })
        values = {
            'company_id': warehouse.company_id,
            'date_planned': self.move_id.date_expected,
            'move_dest_ids': self.move_id,
            'group_id': group_id,
            'route_ids': self.move_id.product_id.route_ids,
            'warehouse_id': warehouse,
        }
        product_qty = self.qty_to_sincan
        product_uom = self.uom
        product = self.product_id
        location = warehouse.lot_stock_id
        origin = self.move_id.picking_id.name or "/"
        priorty = self.priority if self.priority else 1
        self.env['procurement.group']._run(
            product, product_qty, product_uom, location, "/", origin, values, priorty)

    @api.multi
    def create_procurement_merkez(self):
        self.ensure_one()
        warehouse = self.env['stock.warehouse'].search([('id', '=', 1)])
        group_id = self.env["procurement.group"].create({
            'name': u"%s" % (warehouse.name) + " Açan: " + self.env.user.name,
        })
        values = {
            'company_id': warehouse.company_id,
            'date_planned': self.move_id.date_expected,
            'move_dest_ids': self.move_id,
            'group_id': group_id,
            'route_ids': self.move_id.product_id.route_ids,
            'warehouse_id': warehouse,
        }
        product_qty = self.qty_to_merkez
        product_uom = self.uom
        product = self.product_id
        location = warehouse.lot_stock_id
        origin = self.move_id.picking_id.name or "/"
        priorty = self.priority if self.priority else 1
        self.env['procurement.group']._run(
            product, product_qty, product_uom, location, "/", origin, values, priorty)
