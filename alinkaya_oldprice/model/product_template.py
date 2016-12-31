# -*- encoding: utf-8 -*-

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp


class product_template(osv.Model):
    _inherit = 'product.template'
    _columns = {
        'z_fiyat_2015a': fields.float(
             u"2015 Ocak Eski Fiyatı",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2015 Ocak eski fiyatı"),
        'z_2015a_iscilik': fields.float(
             u"2015 Ocak işçilik Fiyatı",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2015 Ocak kullanılan birim işçilik fiyatı"),
        'z_min_2015a_iscilik': fields.float(
             u"2015 Ocak Min İşçcilik",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2015 Ocak kullanılan eski Minimum İşçilik fiyatı"),
        'z_fiyat_2014': fields.float(
             u"2014 Eski Fiyatı",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2014 yılında kullanilan eski fiyatı"),
        'z_2014_iscilik': fields.float(
             u"2014 işçilik Fiyatı",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2014 yılında kullanılan birim işçilik fiyatı"),
        'z_min_2014_iscilik': fields.float(
             u"2014 Min İşçcilik Fiyatı",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2014 yılında kullanılan eski Minimum İşçilik fiyatı"),
        'z_fiyat_2016a': fields.float(
            u"2015 Ekim Fiyatı",
            digits_compute=dp.get_precision('Product Price'),
            help=u"2015 Ekim fiyati"),
        'z_2016a_iscilik': fields.float(
            u"2015 Ekim isçilik fiyatı",
            digits_compute=dp.get_precision('Product Price'),
            help=u"2015 Ekim birim işçilik fiyatı"),
        'z_min_2016a_iscilik': fields.float(
            u"2015 Ekim Min İscilik",
            digits_compute=dp.get_precision('Product Price'),
            help=u" kullanılan eski Minimum İscilik fiyatıı"),
    }
product_template()