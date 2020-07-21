from odoo import models, fields, api
from odoo.tools import float_is_zero




#TODO @dogan:  not ported should check onur
class StockMove(models.Model):
    _inherit = 'stock.move'

    qty_available_sincan = fields.Float('Sincan Depo Mevcut', related='product_id.qty_available_sincan')
    qty_available_merkez = fields.Float('Merkez Depo Mevcut', related='product_id.qty_available_merkez')

#TODO: check method
    # @api.model
    # def _prepare_procurement_from_move(self, move):
    #     res = super(StockMove, self)._prepare_procurement_from_move(move)
    #     if res and 'sale_line_id' not in res:
    #         sale_line_id = move.procurement_id.sale_line_id.id or move.raw_material_production_id.move_prod_id.procurement_id.sale_line_id.id
    #         res.update({'sale_line_id': sale_line_id})
    #
    #     return res

    @api.multi
    def action_create_procurement(self):
        self.ensure_one()
        warehouses = self.env['stock.warehouse'].search([('selectable_on_procurement_wizard', '=', True)])
        if warehouses:
            qty_lines = [(0, 0, {
                'warehouse_id': wh.id,
                'warehouse_id_readonly': wh.id
            }) for wh in warehouses]
        else:
            qty_lines = []
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.procurement.move',
            'context': {'default_move_id': self.id, 'default_procurement_qty_ids': qty_lines},
            'target': 'new'
        }

    @api.multi
    def action_make_mts(self):
        self.ensure_one()
        return {
            'name': 'Pick from stock',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'make.mts.move',
            'context': {'default_move_id': self.id},
            'target': 'new'
        }

    @api.multi
    def action_view_origin_moves(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.name,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'stock.move',
            'domain': [('move_dest_ids', 'in', self.id)],
            'target': 'current'
        }

    # TODO: check method
    # @api.model
    # def _create_procurements(self, moves):
    #     res = super(StockMove, self)._create_procurements(moves)
    #     moves_to_remove = []
    #     for move in moves:
    #         if move.procure_method == 'make_to_stock':
    #             moves_to_remove.append(move)
    #
    #     for tm in moves_to_remove:
    #         moves.remove(tm)
    #
    #     return res






    # def _get_invoice_line_vals(self, cr, uid, move, partner, inv_type, context=None):
    #     res = super(StockMove, self)._get_invoice_line_vals(cr, uid, move, partner, inv_type, context=context)
    #     if inv_type in ('out_invoice', 'out_refund') and not move.procurement_id:
    #         operation_move = move.mapped('linked_move_operation_ids.operation_id.linked_move_operation_ids.move_id').filtered(lambda m:m.product_id.id == move.product_id.id and m.procurement_id.sale_line_id.id)
    #
    #         try:
    #             sale_move = operation_move[0]
    #         except IndexError:
    #             try:
    #                 sale_moves = move.picking_id.move_lines.filtered(lambda m:m.product_id.id == move.product_id.id and m.procurement_id.sale_line_id.id and m.id != move.id)
    #                 sale_move = sale_moves[0]
    #             except IndexError:
    #                 pass
    #                 return res
    #
    #         sale_line = sale_move.procurement_id.sale_line_id
    #         res['invoice_line_tax_id'] = [(6, 0, [x.id for x in sale_line.tax_id])]
    #         res['account_analytic_id'] = sale_line.order_id.project_id and sale_line.order_id.project_id.id or False
    #         res['discount'] = sale_line.discount
    #         if move.product_id.id != sale_line.product_id.id:
    #             precision = self.env['decimal.precision'].precision_get(cr, uid, 'Discount')
    #             if float_is_zero(sale_line.discount, precision_digits=precision):
    #                 res['price_unit'] = self.env['product.pricelist'].price_get(
    #                     cr, uid, [sale_line.order_id.pricelist_id.id],
    #                     move.product_id.id, move.product_uom_qty or 1.0,
    #                     sale_line.order_id.partner_id, context=context)[sale_line.order_id.pricelist_id.id]
    #             else:
    #                 res['price_unit'] = move.product_id.lst_price
    #         else:
    #             res['price_unit'] = sale_line.price_unit
    #         uos_coeff = move.product_uom_qty and move.product_uos_qty / move.product_uom_qty or 1.0
    #         res['price_unit'] = res['price_unit'] / uos_coeff
    #
    #     return res
    
    

    # def action_done(self, cr, uid, ids, context=None):
    #     res = super(StockMove, self).action_done(cr, uid, ids, context=context)
    #     moves = self.browse(cr, uid, ids, context=context)
    #
    #     mapping = {}
    #     for move in moves.filtered(lambda m: m.state == 'done' and m.move_dest_id.id):
    #         origin = False
    #         if move.production_id.id:
    #             origin = move.production_id
    #         elif move.picking_id.id:
    #             origin = move.picking_id
    #
    #         dest_pickings = mapping.get(origin, set())
    #         if move.move_dest_id.picking_id:
    #             dest_pickings.add(move.move_dest_id.picking_id)
    #         mapping[origin] = dest_pickings
    #
    #     for src_obj, dest_pickings in mapping.iteritems():
    #         if not src_obj.origin or len(src_obj.origin) == 0:
    #             # origin document is the source
    #             origin = src_obj.name
    #         else:
    #             origin = re.findall('##[^#]*##', src_obj.origin)
    #             if len(origin) == 0:
    #                 #origin is not empty bu no ## defined so take self as origin.
    #                 origin = src_obj.name
    #             else:
    #                 if len(origin[0])>5:
    #                     origin = origin[0][2:-2]
    #                 else:
    #                     origin = src_obj.name
    #
    #         for picking in dest_pickings:
    #             existing_origin = re.findall('##[^#]*##', picking.origin or '')
    #             combined_origin = ""
    #             if len(existing_origin) > 0:
    #                 existing_origin = existing_origin[0][2:-2]
    #                 existing_origins = existing_origin.split(",")
    #                 existing_origins.append(origin)
    #                 origins=set(existing_origins)
    #                 combined_origin=",".join(origins)
    #             else:
    #                 combined_origin=origin
    #             old_origin = picking.origin or ""
    #             picking.origin = '%s##%s##' % (re.sub('##[^#]*##', '', old_origin) or '', combined_origin)
    #
    #
    #     for picking in moves.mapped('picking_id').filtered(lambda p: p.state == 'done'):
    #         picking.origin = re.sub('##[^#]*##', '', picking.origin)
    #
    #     return res
        
    

