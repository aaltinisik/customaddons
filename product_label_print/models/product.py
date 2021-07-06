# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date

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
    batch_code = fields.Char(string='Batch Code', compute='gen_batch_code', store=False)
    day_code = {
        '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8',
        '9': '9', '10': 'a', '11': 'b', '12': 'c',
        '13': 'd', '14': 'e', '15': 'f', '16': 'g',
        '17': 'h', '18': 'i', '19': 'j', '20': 'k',
        '21': 'l', '22': 'm', '23': 'n', '24': 'o',
        '25': 'p', '26': 'r', '27': 's', '28': 't',
        '29': 'u', '30': 'v', '31': 'y',}
    month_code = {
        '1': 'a', '2': 's', '3': 'd', '4': 'f',
        '5': 'g', '6': 'h', '7': 'j', '8': 'k',
        '9': 'l', '10': 'z', '11': 'x', '12': 'c',
    }
    year_code = {
        '2019': 'Q', '2020': 'W', '2021': 'E', '2022': 'R', '2023': 'T', '2024': 'Y', '2025': 'U', '2026': 'I',
        '2027': 'O', '2028': 'P', '2029': 'A', '2030': 'S', '2031': 'D', '2032': 'F', '2033': 'G', '2034': 'H',
        '2035': 'J', '2036': 'K', '2037': 'L', '2038': 'Z', '2039': 'X', '2040': 'C', '2041': 'V', '2042': 'B',
    }

    @api.depends('batch_code')
    def gen_batch_code(self):
        today = date.today()
        self.batch_code = "%s%s%s%s" % (self.day_code[str(today.day)],
                                        self.month_code[str(today.month)],
                                        self.year_code[str(today.year)],
                                        (self.env.user.id % 20 + 17))


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
