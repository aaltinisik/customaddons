# -*- coding: utf-8 -*-

from openerp import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    group_id = fields.Many2one('procurement.group',string='Producrement Group', copy=False)#, related='move_prod_id.group_id')

    mo_printed = fields.Boolean('Manufacting Order Printed', default=False)

    @api.onchange('routing_id')
    def onchange_routing_id(self):
        if self.routing_id.location_id:
            self.location_src_id = self.routing_id.location_id
            self.location_dest_id = self.routing_id.location_id
            
            
    @api.model
    def _make_consume_line_from_data(self, production, product, uom_id, qty,
                                     uos_id, uos_qty):
        move_id = super(MrpProduction, self)._make_consume_line_from_data(
            production, product, uom_id, qty, uos_id, uos_qty)
        self.env['stock.move'].browse([move_id]).priority = production.priority
        return move_id
    
    
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

    @api.model
    def auto_print_mrp_orders(self):
        productions = self.search([('routing_id', '=', 'Profil Kesim'),
                                ('state', 'in', ['confirmed', 'ready', 'in_production', 'done']),
                                ('mo_printed', '=', False)],
                                  limit=20)
        report = self.pool.get('report')
        #produce_object = self.pool.get('mrp.produce.more')
        cr, uid, context = self._cr, self._uid,self._context,

        for production in productions:

            report.print_document(cr, uid, [production.id], 'altinkaya.report_mrporder_altinkayaE', html=None,
                                  data=None,
                                  context=context)
#            produce_object.produce_mrp_order(cr, uid, [production.id], context=context)
            production.write({'mo_printed': True})
            
            
    @api.model
    def create(self, vals):
        if 'group_id' not in vals:
            group_id = self.env['procurement.group'].create({'name':'Manually created by %s at %s' % (self.env.user.name, fields.Datetime.now())})
            vals.update({'group_id':group_id.id})
            
        return super(MrpProduction, self).create(vals)
            
    
