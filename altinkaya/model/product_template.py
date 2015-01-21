# -*- encoding: utf-8 -*-

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp


class product_template(osv.Model):
    _inherit = 'product.template'
    _columns = {
        'x_default_code': fields.char(
            'Sablon Referansi',
            size=64,
            required=False),
        'x_fiyat_dolar': fields.float(
             'Dolar Fiyati',
             digits_compute=dp.get_precision('Product Price'),
             help="Dolarla satilan urunlerin fiyati bu alana gore yapilir"),
        'x_fiyat_euro': fields.float(
             'Euro Fiyati',
             digits_compute=dp.get_precision('Product Price'),
             help="Euro ile satilirken kullanilan temel fiyat"),
        'z_fiyat_2014': fields.float(
             u'Eski 2014 Fiyatı',
             digits_compute=dp.get_precision('Product Price'),
             help=u"2014 yılında kullanilan eski fiyatı"),
        'z_2014_iscilik': fields.float(
             u'2014 İşçilik Fiyatı',
             digits_compute=dp.get_precision('Product Price'),
             help=u"2014 yılında kullanılan birim işçilik fiyatı"),
        'z_min_2014_iscilik': fields.float(
             u'2014 Min. İşçcilik Fiyatı',
             digits_compute=dp.get_precision('Product Price'),
             help=u"2014 yılında kullanılan eski Minimum İşçilik fiyatı"),
    }
product_template()