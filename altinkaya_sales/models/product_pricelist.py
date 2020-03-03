# -*- encoding: utf-8 -*-
#
#Created on Jan 17, 2020
#
#@author: dogan
#
from odoo import models, fields, api
from odoo.tools.translate import _

class ProductPricelistType(models.Model):
    _name = "product.pricelist.type"
    
    def _compute_selection_fields(self):
        res = []
        fields = self.env['ir.model.fields'].search([('model','in',['product.product']),('ttype','=','float')])
        for field in fields:
            if not (field.name,field.field_description) in res:
                res.append((field.name,field.field_description))
        return res
    
    name = fields.Char(string="Name",required=True)
    field = fields.Selection(selection = lambda self:self._compute_selection_fields(),string="Field",required=True)
    active = fields.Boolean(string="Active",default=True)


class ProductPriclelistItem(models.Model):
    _inherit = 'product.pricelist.item'
    
    
    def _compute_base(self):
        res = [
        ('list_price', _('Public Price')),
        ('standard_price', _('Cost')),
        ('pricelist', _('Other Pricelist'))]
        
        
        price_types = self.env['product.pricelist.type'].search([('active','=',True)])
        for price_type in price_types:
            if not (price_type.field,price_type.name) in res:
                res.append((price_type.field,price_type.name))    
        return res        
                
    x_guncelleme = fields.Char('Guncelleme Kodu',size=64)
    base = fields.Selection(selection = lambda self: self._compute_base())
    
    
    