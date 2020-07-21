# -*- coding: utf-8 -*-
#
#Created on Oct 12, 2018
#
#@author: dogan
#

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class MakeMtsMove(models.TransientModel):
    _name = 'make.mts.move'

    move_id = fields.Many2one('stock.move','Move', readonly=True)
    #cancel_production_ids = fields.Many2many('mrp.production',compute='_compute_productions', string='Productions to be canceled')
    #cancel_move_ids = fields.Many2many('stock.move',compute='_compute_productions', string='Productions to be canceled')
    
    #cancel_procurement_ids = fields.Many2many('procurement.order',string='Procurements to cancel', compute='_compute_procurements')
    
    
    #@api.one
    #def _compute_procurements(self):
    #    self.move_orig_ids.

    def find_orig_move_ids(self,moves):
        orig_moves = moves
        for move in moves:
            orig_moves |= self.find_orig_move_ids(move.move_orig_ids)
        return orig_moves

    def cancel_move_origs(self, move_id):
        moves_with_origs = self.find_orig_move_ids(move_id)
        moves_with_origs = moves_with_origs.filtered(lambda m: m.state not in ['done', 'cancel'])
        # set the propagate field to False, so it will be possible to cancel the moves separately.
        moves_with_origs.write({'propagate': False})
        moves_no_production = moves_with_origs.filtered(lambda m: not m.production_id)
        productions = moves_with_origs.mapped('production_id')
        productions.filtered(lambda p: p.state not in ['progress', 'done', 'cancel']).action_cancel()
        moves_no_production._action_cancel()

    @api.multi
    def action_confirm(self):
        self.ensure_one()
        sale_order = self.move_id.sale_line_id.order_id
        order_state = sale_order.state
        #invoice_state = self.invoice_status

        self.cancel_move_origs(self.move_id)
        #self.move_id._action_cancel()
        self.move_id.procure_method = 'make_to_stock'
        self.move_id.move_orig_ids = False
        self.move_id._action_confirm()
        self.move_id._action_assign()
        
        # if order_state != 'shipping_except' and sale_order.state == 'shipping_except':
        #     sale_order.state = order_state

        # if invoice_state != self.move_id.invoice_state:
        #     self.move_id.invoice_state = invoice_state
                
        return {}

