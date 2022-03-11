# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    is_difference_invoice = fields.Boolean(string='Is Difference Invoice')
    difference_amount = fields.Monetary(string='Difference Amount')
