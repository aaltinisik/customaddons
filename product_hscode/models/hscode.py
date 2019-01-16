# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductHscode(models.Model):
    _name = 'product.hscode'
    _order = "hscode"
    
    
    
    name = fields.Char('Name',required=True, size=100)
    hscode = fields.Char('GTIP', size=16)
    nameen = fields.Char('Name(Eng)', size=100)
    short_desc = fields.Char('Short Description', size=50)
    long_desc = fields.Char('Long Description', size=200)
    Kisa_aciklama = fields.Char('Kısa Açıklama', size=50)
    Uzun_aciklama = fields.Char('Uzun Açıklama', size=200)
    image = fields.Binary("Image")
    notes = fields.Text('Notes')

    




