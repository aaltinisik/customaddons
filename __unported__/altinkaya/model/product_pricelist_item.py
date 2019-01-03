from openerp.osv import osv, fields


class product_pricelist_item(osv.Model):
    _inherit = 'product.pricelist.item'
    _columns = {
        'x_guncelleme': fields.char(
            'Guncelleme Kodu',
            size=64,
            required=False),
    }
product_pricelist_item()