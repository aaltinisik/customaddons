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
        'z_fiyat_2016a': fields.float(
             u"2016 Aralik Eski Fiyati",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2016 Aralik eski fiyati"),
        'z_2016a_iscilik': fields.float(
             u"2016 Aralik iscilik Fiyati",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2016 Aralik kullanılan birim iscilik fiyatı"),
        'z_min_2016a_iscilik': fields.float(
             u"2016 Aralik Min İscilik",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2016 Aralık kullanılan eski Minimum İscilik fiyatı"),



    }
product_template()
