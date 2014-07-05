from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp


class product_product(osv.Model):
    _inherit = 'product.product'
    _name = 'product.product'
    _columns = {
        'x_cari_urun': fields.many2one(
            'res.partner',
            'Carinin Urunu'
            ),
        'x_iscilik': fields.float(
             'iscilik Fiyati',
             digits_compute=dp.get_precision('Product Price'),
             help="Birim iscilik Fiyati"),
        'x_min_iscilik': fields.float(
             'Minimum iscilik Fiyati',
             digits_compute=dp.get_precision('Product Price'),
             help="En Az Toplam iscilik Fiyati"),
    }
product_product()
