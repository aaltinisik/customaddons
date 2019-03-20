# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class productproductLabel(models.TransientModel):
    _name = "product.product.label"
    _description="Product Product Label"
    
    name = fields.Char(string="Name",size=120)
    nameL1 = fields.Char(string="NameL1",size=30)
    nameL2 = fields.Char(string="NameL2", size=30)
    nameL3 = fields.Char(string="NameL3", size=30)
    nameL4 = fields.Char(string="NameL4", size=30)
    default_code = fields.Char(string="Default_code",size=40)
    short_code = fields.Char(string="Short Code",size=20)
    note = fields.Char(string="Note",size=40)
    pieces_in_pack = fields.Float(string="# in Cartoon")
    label_to_print = fields.Integer(string='# of label to be printed', default=1)
    product_id = fields.Many2one('product.product', string="Product")
    barcode = fields.Char(string="Barcode")
    uom_name = fields.Char(string="UOM Name", size=10)


class labelTwoinrow(models.TransientModel):
    _name = "label.twoinrow"
    _description="Label Two in Row"
    
    first_label_empty = fields.Boolean("Skip first label in row")
    second_label_empty = fields.Boolean("Skip second label in row")
    label1 = fields.Many2one('product.product.label', string="Label 1")
    label2 = fields.Many2one('product.product.label', string="Label 2")
    copies_to_print = fields.Integer(string='# of label to be printed', default=1)


class product_product(models.Model):
    _inherit = 'product.product'
    
    @api.multi
    def action_print_label(self):
        aw_obj = self.env['ir.actions.act_window'].with_context({'default_restrict_single':True})
        action = aw_obj.for_xml_id('product_label_print', 'action_print_pack_barcode_wiz')
        action.update({'context':{'default_restrict_single':True}})
        return action
        
        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
