# -*- coding: utf-8 -*-

from openerp import api, fields, models, _


class productproductLabel(models.TransientModel):
    _name = "product.product.label"
    name = fields.Char(string="Name", size=120)
    default_code = fields.Char(string="Default_code", size=40)
    short_code = fields.Char(string="Short Code", size=20)
    note = fields.Char(string="Note", size=40)
    pieces_in_pack = fields.Float(string="# in Cartoon")
    label_to_print = fields.Integer(string='# of label to be printed', default=1)
    product_id = fields.Many2one('product.product', string="Product")
    barcode = fields.Char(string="Barcode")
    no_of_products = fields.Float(string='# of products')

    @api.onchange('pieces_in_pack', 'no_of_products')
    def onchange_product(self):
        if self.pieces_in_pack or self.no_of_products:
            x = round(self.no_of_products / self.pieces_in_pack if self.pieces_in_pack > 0 else 1)
            self.label_to_print = x if x > 0 else 1


class labelTwoinrow(models.TransientModel):

    _name = "label.twoinrow"
    first_label_empty = fields.Boolean("Skip first label in row")
    second_label_empty = fields.Boolean("Skip second label in row")
    label1 = fields.Many2one('product.product.label', string="Label")
    label2 = fields.Many2one('product.product.label', string="Label 2")
    copies_to_print = fields.Integer(string='# of label to be printed', default=1)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
