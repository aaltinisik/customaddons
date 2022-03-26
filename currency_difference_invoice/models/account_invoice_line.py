# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.invoice.line'

    moves_to_reconcile = fields.Many2many(comodel_name='account.move.line', string='Moves to reconcile')
    difference_base_move_id = fields.Many2one(comodel_name='account.move.line', string='Difference base move')
