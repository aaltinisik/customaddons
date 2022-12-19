# -*- encoding: utf-8 -*-

from odoo import models, fields,api
from odoo.addons import decimal_precision as dp

class productProduct(models.Model):
    _inherit = 'product.product'
    
    v_fiyat_2015a = fields.Float("2015 Ocak Eski Fiyatı TL",digits=dp.get_precision('Product Price'),help="2015 Ocak eski fiyatı")
    v_2015a_iscilik = fields.Float("2015 Ocak işçilik Fiyatı TL",digits=dp.get_precision('Product Price'),help=u"2015 Ocak kullanılan birim işçilik fiyatı")
    v_min_2015a_iscilik = fields.Float("2015 Ocak Min İşçcilik TL",digits=dp.get_precision('Product Price'), help=u"2015 Ocak kullanılan eski Minimum İşçilik fiyatı TL")
    v_fiyat_2014 = fields.Float(u"2014 Eski Fiyatı TL",digits=dp.get_precision('Product Price'),help=u"2014 yılında kullanılan eski fiyatı TL")
    v_2014_iscilik = fields.Float("2014 işçilik Fiyatı TL",digits=dp.get_precision('Product Price'),help=u"2014 yılında kullanılan birim işçilik fiyatı TL")
    v_min_2014_iscilik = fields.Float("2014 Min İşçcilik Fiyatı TL",digits=dp.get_precision('Product Price'),help=u"2014 yılında kullanılan eski Minimum İşçilik fiyatı TL")
    v_fiyat_2016a = fields.Float("2015 Ekim Fiyatı TL",digits=dp.get_precision('Product Price'),help=u"2015 Ekim fiyati TL")
    v_2016a_iscilik = fields.Float("2015 Ekim isçilik fiyatı TL",digits=dp.get_precision('Product Price'),help=u"2015 Ekim birim işçilik fiyatı TL")
    v_min_2016a_iscilik = fields.Float("2015 Ekim Min İscilik TL",digits=dp.get_precision('Product Price'),help=u" kullanılan eski Minimum İşcilik fiyatı TL")
    v_fiyat_2016b = fields.Float("2016 Aralık Fiyatı TL",digits=dp.get_precision('Product Price'),help=u"2016 Aralık fiyatı TL")
    v_2016b_iscilik = fields.Float("2016 Aralık isçilik fiyatı TL",digits=dp.get_precision('Product Price'),help=u"2016 Aralık birim işçilik fiyatı TL")
    v_min_2016b_iscilik = fields.Float("2016 Aralık Min İsçilik TL",digits=dp.get_precision('Product Price'),help=u"2016 Aralık Minimum İşçilik fiyatı TL")
    v_fiyat_2017 = fields.Float("2017 Aralık Fiyatı TL",digits=dp.get_precision('Product Price'),help=u"2017 Aralık fiyatı TL")
    v_2017_iscilik = fields.Float(u"2017 Aralık isçilik fiyatı TL",digits=dp.get_precision('Product Price'),help=u"2017 Aralık birim işçilik fiyatı TL")
    v_min_2017_iscilik = fields.Float(u"2017 Aralık Min İsçilik TL",digits=dp.get_precision('Product Price'),help=u"2017 Aralık Minimum İşçilik fiyatı TL")
    attr_price =  fields.Float(compute="_compute_attr_based_price", digits=dp.get_precision('Product Price'), string=u"Attr. Value Price",help=u"Price calculated based on the product's attribute values.")
    purchase_price = fields.Float("Satınalma Fiyatı",digits=dp.get_precision('Product Price'),help="Satınalma Fiyatı")
    v_cari_urun = fields.Many2one('res.partner',"Partner Product")
    v_tl_fiyat = fields.Float("USD Fiyatı",digits=dp.get_precision('Product Price'),help="Birim işçilik Fiyatı USD")
    v_iscilik_fiyat = fields.Float("işçilik Fiyatı USD",digits=dp.get_precision('Product Price'),help=u"Birim işçilik Fiyatı USD")
    v_min_iscilik_fiy = fields.Float('Minimum işçilik Fiyatı USD',digits=dp.get_precision('Product Price'),help="En Az Toplam işçilik Fiyatı USD")
    v_guncel_fiyat = fields.Boolean("Fiyat Güncel", help="Bu seçenek seçili ise fiyatı yenidir.")
    name_variant =fields.Char(compute="_compute_name_variant_report_name",string='Variant Name')
    
    #altinkaya
    v_fiyat_dolar = fields.Float("Dolar Fiyatı",digits=dp.get_precision('Product Price'),help="Dolarla satılan ürünlerin fiyatı")
    v_fiyat_euro = fields.Float("Euro Fiyatı",digits=dp.get_precision('Product Price'),help="Euro ile satılırken kullanılan temel fiyat")

    @api.depends('product_tmpl_id')
    def _compute_attr_based_price(self):
        res = {}
        for product in self:
            priced_attributes = { al.attribute_id.id:{'base_price':al.attr_base_price,
                                                      'price_coef': al.attr_val_price_coef} for al in product.product_tmpl_id.attribute_line_ids.filtered(lambda al: al.use_in_pricing)}
            
            val = 0.0
            for att_val in product.attribute_value_ids:
                if att_val.attribute_id.id in priced_attributes:
                    val += priced_attributes[att_val.attribute_id.id]['base_price'] +  priced_attributes[att_val.attribute_id.id]['price_coef'] * att_val.numeric_value
            if val is 0.0:
                val = product.v_fiyat_dolar
            product.attr_price = val
            
    
    @api.multi
    def _compute_name_variant_report_name(self):
        result = self.with_context({'display_default_code':False}).name_get()
        return result
