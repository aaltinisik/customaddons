# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.invoice.line'

    difference_base_aml_id = fields.Many2one(comodel_name='account.move.line', string='Difference base move')
