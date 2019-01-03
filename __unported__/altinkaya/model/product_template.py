# -*- encoding: utf-8 -*-

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp


class product_template(osv.Model):
    _inherit = 'product.template'
    _columns = {
        # 'x_default_code': fields.char(
        #     'Sablon Referansi',
        #     size=64,
        #     required=False),
        # 'x_fiyat_dolar': fields.float(
        #      'x Dolar Fiyati',
        #      digits_compute=dp.get_precision('Product Price'),
        #      help="Dolarla satilan urunlerin fiyati bu alana gore yapilir"),
        # 'x_fiyat_euro': fields.float(
        #      'x Euro Fiyati',
        #      digits_compute=dp.get_precision('Product Price'),
        #      help="Euro ile satilirken kullanilan temel fiyat"),
    }
product_template()
class productProduct(osv.Model):
    _inherit = 'product.product'
    _columns = {
        'v_fiyat_dolar': fields.float(
             u"Dolar Fiyatı",
             digits_compute=dp.get_precision('Product Price'),
             help=u"Dolarla satılan ürünlerin fiyatı"),
        'v_fiyat_euro': fields.float(
             u"Euro Fiyatı",
             digits_compute=dp.get_precision('Product Price'),
             help=u"Euro ile satılırken kullanılan temel fiyat"),
    }
productProduct()