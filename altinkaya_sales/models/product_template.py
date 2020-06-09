'''
Created on Jan 17, 2019

@author: cq
'''
from odoo import models,fields,api
from odoo.addons import decimal_precision as dp
from odoo.tools.func import default

#Aktarıldı
class product_attribute_line(models.Model):
    _inherit = 'product.template.attribute.line'
    attr_base_price =fields.Float(
             u"Base Price",
             digits=dp.get_precision('Product Price'),
             help=u"Base price used to compute product price based on attribute value.")
    attr_val_price_coef= fields.Float(
             u"Value Price Multiplier",
             digits=dp.get_precision('Product Price'),
             help=u"Attribute value coefficient used to compute product price based on attribute value.")
    use_in_pricing = fields.Boolean('Use in pricing')
    

class ProductTemplate(models.Model):
    _inherit='product.template'
    
    
    #for sale configurator
    attr_price =  fields.Float(digits=dp.get_precision('Product Price'), string=u"Attr. Value Price",help=u"Price calculated based on the product's attribute values.",default=0.0)
    v_tl_fiyat = fields.Float("USD Fiyatı",digits=dp.get_precision('Product Price'),help="Birim işçilik Fiyatı USD",default=0.0)
    v_iscilik_fiyat = fields.Float("işçilik Fiyatı USD",digits=dp.get_precision('Product Price'),help=u"Birim işçilik Fiyatı USD",default=0.0)
    v_min_iscilik_fiy = fields.Float('Minimum işçilik Fiyatı USD',digits=dp.get_precision('Product Price'),help="En Az Toplam işçilik Fiyatı USD",default=0.0)
    v_guncel_fiyat = fields.Boolean("Fiyat Güncel", help="Bu seçenek seçili ise fiyatı yenidir.",default=0.0)
    
    #altinkaya
    v_fiyat_dolar = fields.Float("Dolar Fiyatı",digits=dp.get_precision('Product Price'),help="Dolarla satılan ürünlerin fiyatı",default=0.0)
    v_fiyat_euro = fields.Float("Euro Fiyatı",digits=dp.get_precision('Product Price'),help="Euro ile satılırken kullanılan temel fiyat",default=0.0)
    
    has_production_bom = fields.Boolean('Has production BoM',compute='_compute_has_production_bom', store=True)
    
    @api.one
    @api.depends('bom_ids','bom_ids.type')
    def _compute_has_production_bom(self):
        self.has_production_bom = any(self.bom_ids.filtered(lambda b: b.type != 'phantom'))
        


