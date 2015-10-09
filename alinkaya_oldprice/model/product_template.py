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
             u"2014 işçilik Fiyatı",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2015 Ocak kullanılan birim işçilik fiyatı"),
        'z_min_2015a_iscilik': fields.float(
             u"2015 Min İşçcilik Fiyatı",
             digits_compute=dp.get_precision('Product Price'),
             help=u"2015 Ocak kullanılan eski Minimum İşçilik fiyatı"),
    }
product_template()