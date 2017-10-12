# -*- coding: utf-8 -*-

from openerp import api, fields, models, _


class productproductLabel(models.Model):
    _name = "product.product.label"

    name = fields.Char(string="Name")
    default_code = fields.Char(string="Default_code")
    note = fields.Text(string="Note")
    pieces_in_pack = fields.Float(string="# in Cartoon")
    label_to_print = fields.Integer(string='# of label to be printed', default=1)
    product_id = fields.Many2one('product.product', string="Product")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
