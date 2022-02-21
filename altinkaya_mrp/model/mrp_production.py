# -*- coding: utf-8 -*-

from odoo import models, fields, api


#TODO: @dogan bence bu verilerin workcentera tasinmasi gerek uzerinde olmasi gerekli.
class x_makine(models.Model):
    _name = 'x.makine'
    _description="X Makine"


    x_group = fields.Char(
            'Bölüm',
            size=128,
            )
    x_kod =  fields.Char(
            'Makine Kodu',
            size=128)
    x_name = fields.Char(
            'Makine Adı',
            size=128)
    name =  fields.Char(
            'Makine Numarası',
            size=128)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    #group_id = fields.Many2one('procurement.group',string='Producrement Group', related='move_prod_id.group_id')
    mo_printed = fields.Boolean('Manufacting Order Printed', default=False)
    sale_id = fields.Many2one('sale.order',string="Sale Order")
    
    date_planned = fields.Datetime('Scheduled Date')
    date_start2 = fields.Datetime('Start Date')
    date_finished2 = fields.Datetime('End Date')
    priority = fields.Selection([('0','Not urgent'),('1','Normal'),('2','Urgent'),('3','Very Urgent')],string='Priority',default="0")
    process_id = fields.Many2one('mrp.routing', string='Rota', readonly=True, compute='_get_process_id', store=True)
    x_operator = fields.Many2one(
            'hr.employee',
            'Uretimi Yapan Operator'
            )
    x_note = fields.Text(
            'Not',
            size=256)
    #TODO: @dogan workcenter_id alanini kullanabiliriz
    x_makine = fields.Many2one('x.makine',
            'Uretim Yapilan Makine'
            )
    x_makine_kod =  fields.Char(related='x_makine.x_kod',
            string='Makine',
            readonly=1)
    procurement_group_name = fields.Char(compute='_get_procurement_group_name',string="Procurement Group",readonly=True)
    product_pickings = fields.Many2many(compute="_get_product_pickings",string="Product Pickings", relation='stock.picking',
             readonly=True)

    @api.multi
    def _get_process_id(self):
        for production in self:
            production.process_id = production.bom_id.routing_id.id

    @api.model
    def _update_existing_record(self):
        productions = self.env['mrp.production'].search([('process_id', '=', False)])
        for production in productions:
            production.process_id = production.bom_id.routing_id.id

    @api.multi
    def _generate_moves(self):
        if self.env.context.get("context",{}).get("migration",False):
            return True
        for production in self:
            production._generate_finished_moves()
            factor = production.product_uom_id._compute_quantity(production.product_qty, production.bom_id.product_uom_id) / production.bom_id.product_qty
            boms, lines = production.bom_id.explode(production.product_id, factor, picking_type=production.bom_id.picking_type_id)
            production._generate_raw_moves(lines)
            # Check for all draft moves whether they are mto or not
            production._adjust_procure_method()
            production.move_raw_ids._action_confirm()
        return True
    
    
    def _get_procurement_group_name(self):
        for mo in self:
            if mo.move_finished_ids:
                mo.id = mo.move_finished_ids[0].group_id.name
            else:
                mo.id = False
    
    def get_product_route(self):
        def _get_next_moves(move_id):
            if move_id:
                next_moves = _get_next_moves(move_id.move_dest_ids)
                if next_moves:
                    return move_id | next_moves
                else:
                    return move_id
            return False
        
        if self.move_finished_ids:
            route = []
            for m in _get_next_moves(self.move_finished_ids[0]):
                if m.picking_id.id:
                    route.append(('picking',m.picking_id))
                elif m.raw_material_production_id.id:
                    route.append(('production',m.raw_material_production_id))
                
            res = route
        else:
            res = False
                
        return res

    
    def _get_product_pickings(self):
        def _get_next_moves(move_id):
            if move_id:
                next_moves = _get_next_moves(move_id.move_dest_id)
                if next_moves:
                    return move_id | next_moves
                else:
                    return move_id
            return False
        
        for mo in self:
            if mo.move_finished_ids:
                mo.id = _get_next_moves(mo.move_finished_ids[0]).mapped('picking_id')
            else:
                mo.id = False
    
    
    
    def name_search(self,name, args=None, operator='ilike', limit=80):
        if name:
            args += [('move_finished_ids[0].group_id.name', operator, name)]
        ids = self.search( args, limit=limit)
        return ids.name_get()


    
    
    @api.onchange('routing_id')
    def onchange_routing_id(self):
        if self.routing_id.location_id:
            self.location_src_id = self.routing_id.location_id
            self.location_dest_id = self.routing_id.location_id
    
    

    @api.model
    def create(self, values):
        production = super(MrpProduction, self).create(values)
        def _get_sale_line(moves):
            if moves and moves[0].sale_line_id:
                return moves[0].sale_line_id
            if moves and moves[0].move_dest_ids:
                return _get_sale_line(moves[0].move_dest_ids)
            return False
        
        sale_line = _get_sale_line(production.move_finished_ids and production.move_finished_ids[0])
        if sale_line:
            production.write({
                'sale_id':sale_line.order_id.id or '',
                })

        return production
            
#     @api.model
#     def _make_consume_line_from_data(self, production, product, uom_id, qty,
#                                      uos_id, uos_qty):
#         move_id = super(MrpProduction, self)._make_consume_line_from_data(
#             production, product, uom_id, qty, uos_id, uos_qty)
#         self.env['stock.move'].browse([move_id]).priority = production.priority
#         return move_id
    
    
#     @api.multi
#     def action_confirm(self):
#         res = super(MrpProduction, self).action_confirm()
#         self.env.cr.commit()
#         res2 = self.action_assign()
#         return res

    @api.multi
    def button_print_prod_order(self):
        return self.env.ref('mrp.action_report_production_order').report_action(self)
    
    @api.multi
    def action_print_product_label(self):
        self.ensure_one()
        aw_obj = self.env['ir.actions.act_window'].with_context({'default_restrict_single':True})
        action = aw_obj.for_xml_id('product_label_print', 'action_print_pack_barcode_wiz')
        action.update({'context':{'default_restrict_single':True,
                                  'active_ids':[self.product_id.id]}})
        return action



    #TDE Stay Unported
#     @api.model
#     def auto_print_mrp_orders(self):
#         productions = self.search([('routing_id', '=', 'Profil Kesim'),
#                                 ('state', 'in', ['confirmed', 'ready', 'in_production', 'done']),
#                                 ('mo_printed', '=', False)],
#                                   limit=20)
#         report = self.pool.get('report')
#         produce_object = self.pool.get('mrp.produce.more')
#         cr, uid, context = self._cr, self._uid,self._context,
# 
#         for production in productions:
# 
#             report.print_document(cr, uid, [production.id], 'altinkaya.report_mrporder_altinkayaE', html=None,
#                                   data=None,
#                                   context=context)
# #            produce_object.produce_mrp_order(cr, uid, [production.id], context=context)
#             production.write({'mo_printed': True})
            
    
