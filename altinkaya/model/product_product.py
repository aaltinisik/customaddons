from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp


class product_template(osv.Model):
    _inherit = 'product.template'
    _name = 'product.template'
    _columns = {
        'x_cari_urun': fields.many2one(
            'res.partner',
            'Carinin Urunu'
            ),
        'x_iscilik': fields.float(
             'x iscilik Fiyati',
             digits_compute=dp.get_precision('Product Price'),
             help="Birim iscilik Fiyati"),
        'x_min_iscilik': fields.float(
             'x Minimum iscilik Fiyati',
             digits_compute=dp.get_precision('Product Price'),
             help="En Az Toplam iscilik Fiyati"),
        'z_guncel_fiyat': fields.boolean('Fiyat Guncel', help="Bu secenek secili ise fiyati yenidir."),
    }
product_template()

class productProduct(osv.Model):
    _inherit = 'product.product'
    _name = 'product.product'
    _columns = {
        'v_cari_urun': fields.many2one(
            'res.partner',
            'Carinin Urunu'
            ),
        'v_iscilik_fiyat': fields.float(
             'iscilik Fiyati',
             digits_compute=dp.get_precision('Product Price'),
             help="Birim iscilik Fiyati"),
        'v_min_iscilik_fiy': fields.float(
             'Minimum iscilik Fiyati',
             digits_compute=dp.get_precision('Product Price'),
             help="En Az Toplam iscilik Fiyati"),
        'v_guncel_fiyat': fields.boolean('Fiyat Guncel', help="Bu secenek secili ise fiyati yenidir."),
    }
productProduct()

