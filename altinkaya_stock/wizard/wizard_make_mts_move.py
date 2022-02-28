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
    _description = 'make MTS Move'

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
            if move.move_orig_ids:
                orig_moves |= self.find_orig_move_ids(move.move_orig_ids)
            if move.production_id.move_raw_ids:
                orig_moves |= self.find_orig_move_ids(move.production_id.move_raw_ids)
        return orig_moves

    def cancel_move_origs(self, move_id):
        moves_with_origs = self.find_orig_move_ids(move_id)
        moves_with_origs = moves_with_origs.filtered(lambda m: m.state not in ['done', 'cancel'])

        moves_no_production = moves_with_origs.filtered(lambda m: not m.production_id)
        productions = moves_with_origs.mapped('production_id')
        productions = productions.filtered(lambda p: p.state not in ['progress', 'done', 'cancel'])
        for production in productions:
            production.action_cancel()
        moves_no_production._action_cancel()

    @api.multi
    def action_confirm(self):
        self.ensure_one()
        sale_order = self.move_id.sale_line_id.order_id
        order_state = sale_order.state
        #invoice_state = self.invoice_status

        propagate = self.move_id.propagate
        # set the propagate field to False, so it will be possible to cancel the moves separately.
        self.move_id.write({'propagate': False})
        self.cancel_move_origs(self.move_id)
#        self.move_id._action_cancel()
        self.move_id.procure_method = 'make_to_stock'
        self.move_id.propagate = propagate
        self.move_id._action_confirm()
        self.move_id._action_assign()

