# -*- encoding: utf-8 -*-

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp


class product_attribute_line(osv.Model):
    _inherit = 'product.attribute.line'
    _columns = {
        'attr_base_price': fields.float(
             u"Base Price",
             digits_compute=dp.get_precision('Product Price'),
             help=u"Base price used to compute product price based on attribute value."),
        'attr_val_price_coef': fields.float(
             u"Value Price Multiplier",
             digits_compute=dp.get_precision('Product Price'),
             help=u"Attribute value coefficient used to compute product price based on attribute value."),
        'use_in_pricing': fields.boolean('Use in pricing')
    }
    
product_attribute_line()

class productProduct(osv.Model):
    _inherit = 'product.product'
    
    
    def _compute_attr_based_price(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            priced_attributes = { al.attribute_id.id:{'base_price':al.attr_base_price,
                                                      'price_coef': al.attr_val_price_coef} for al in product.product_tmpl_id.attribute_line_ids.filtered(lambda al: al.use_in_pricing)}
            
            val = 0.0
            for att_val in product.attribute_value_ids:
                if att_val.attribute_id.id in priced_attributes:
                    val += priced_attributes[att_val.attribute_id.id]['base_price'] + att_val.numeric_value * priced_attributes[att_val.attribute_id.id]['price_coef']
            
            res[product.id] = val
            
            
        return res

    _columns = {
        'v_fiyat_2015a': fields.float(
             u"2015 Ocak Eski Fiyatı",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2015 Ocak eski fiyatı"),
        'v_2015a_iscilik': fields.float(
             u"2015 Ocak işçilik Fiyatı",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2015 Ocak kullanılan birim işçilik fiyatı"),
        'v_min_2015a_iscilik': fields.float(
             u"2015 Ocak Min İşçcilik",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2015 Ocak kullanılan eski Minimum İşçilik fiyatı"),
        'v_fiyat_2014': fields.float(
             u"2014 Eski Fiyatı",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2014 yılında kullanılan eski fiyatı"),
        'v_2014_iscilik': fields.float(
             u"2014 işçilik Fiyatı",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2014 yılında kullanılan birim işçilik fiyatı"),
        'v_min_2014_iscilik': fields.float(
             u"2014 Min İşçcilik Fiyatı",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2014 yılında kullanılan eski Minimum İşçilik fiyatı"),
        'v_fiyat_2016a': fields.float(
            u"2015 Ekim Fiyatı",
            digits_compute=dp.get_precision('Product Price'),
            help=u"2015 Ekim fiyati"),
        'v_2016a_iscilik': fields.float(
            u"2015 Ekim isçilik fiyatı",
            digits_compute=dp.get_precision('Product Price'),
            help=u"2015 Ekim birim işçilik fiyatı"),
        'v_min_2016a_iscilik': fields.float(
            u"2015 Ekim Min İscilik",
            digits_compute=dp.get_precision('Product Price'),
            help=u" kullanılan eski Minimum İşcilik fiyatı"),
        'v_fiyat_2016b': fields.float(
            u"2016 Aralık Fiyatı",
            digits_compute=dp.get_precision('Product Price'),
            help=u"2016 Aralık fiyatı"),
        'v_2016b_iscilik': fields.float(
            u"2016 Aralık isçilik fiyatı",
            digits_compute=dp.get_precision('Product Price'),
            help=u"2016 Aralık birim işçilik fiyatı"),
        'v_min_2016b_iscilik': fields.float(
            u"2016 Aralık Min İsçilik",
            digits_compute=dp.get_precision('Product Price'),
            help=u"2016 Aralık Minimum İşçilik fiyatı"),
        'attr_price': fields.function(_compute_attr_based_price, digits_compute=dp.get_precision('Product Price'), string=u"Attr. Value Price",
                                      type='float',
#             store={
#                 'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
#                 'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
#             },
            help=u"Price calculated based on the product's attribute values.")

    }
    
    
    
