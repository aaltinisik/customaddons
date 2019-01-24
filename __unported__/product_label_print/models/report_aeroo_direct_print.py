# -*- coding: utf-8 -*-

from odoo import fields, models


class aeroo_printers(models.Model):
    _inherit = 'aeroo.printers'

    type = fields.Char(string='Printer_Type', size=64)
