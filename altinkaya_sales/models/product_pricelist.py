# -*- encoding: utf-8 -*-
#
#Created on Jan 17, 2020
#
#@author: dogan
#
from odoo import models, fields, api


class ProductPriclelistItem(models.Model):
    _inherit = 'product.pricelist.item'
    
    
    x_guncelleme = fields.Char('Guncelleme Kodu',size=64)