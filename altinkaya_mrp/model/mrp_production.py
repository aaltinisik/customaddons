# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    #group_id = fields.Many2one('procurement.group',string='Producrement Group', related='move_prod_id.group_id')
    mo_printed = fields.Boolean('Manufacting Order Printed', default=False)
    sale_id = fields.Many2one('sale.order',string="Sale Order")

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
        
        sale_line = _get_sale_line(production.move_finished_ids[0])
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
            
    
