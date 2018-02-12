# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp


class product_template(osv.Model):
    _inherit = 'product.template'
    _name = 'product.template'
    _columns = {
        # 'x_cari_urun': fields.many2one(
        #     'res.partner',
        #     'Carinin Urunu'
        #     ),
        # 'x_iscilik': fields.float(
        #      'x iscilik Fiyati',
        #      digits_compute=dp.get_precision('Product Price'),
        #      help="Birim iscilik Fiyati"),
        # 'x_min_iscilik': fields.float(
        #      'x Minimum iscilik Fiyati',
        #      digits_compute=dp.get_precision('Product Price'),
        #      help="En Az Toplam iscilik Fiyati"),
        # 'z_guncel_fiyat': fields.boolean(u"Fiyat Güncel", help=u"Bu secenek seçili ise fiyatı yenidir."),
    }
product_template()

class productProduct(osv.Model):
    _inherit = 'product.product'
    _name = 'product.product'
    
    
    def _report_name_get(self, cr, uid, ids, name, args, context=None):
        context = context.copy()
        context.update({'display_default_code':False})
        result = self.name_get(cr,uid,ids,context)
        return result
    
    
    _columns = {
        'v_cari_urun': fields.many2one(
            'res.partner',
            u"Carinin Ürünü"
            ),
        'v_tl_fiyat': fields.float(
            u"TL Fiyatı",
            digits_compute=dp.get_precision('Product Price'),
            help=u"Birim işçilik Fiyatı"),
        'v_iscilik_fiyat': fields.float(
             u"işçilik Fiyatı",
             digits_compute=dp.get_precision('Product Price'),
             help=u"Birim işçilik Fiyatı"),
        'v_min_iscilik_fiy': fields.float(
             'Minimum işçilik Fiyatı',
             digits_compute=dp.get_precision('Product Price'),
             help=u"En Az Toplam işçilik Fiyatı"),
        'v_guncel_fiyat': fields.boolean(u"Fiyat Güncel", help=u"Bu seçenek seçili ise fiyatı yenidir."),
        'name_variant':fields.function(_report_name_get,
                                      string='Variant Name',
                                      type='char', select=1,
                                      readonly=True, store=False),
        'terazi_kodu': fields.char(u'Terazi Kodu', size=4, default=None),

    }

    _sql_constraints = [
        ('uniq_terazi_kodu',
         'unique(terazi_kodu)',
         u'Terazi kodu eşsiz olmalı'),
    ]


productProduct()

