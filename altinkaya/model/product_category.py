from openerp.osv import osv, fields


class product_category(osv.Model):
    _inherit = 'product.category'
    _columns = {
        'x_guncelleme': fields.char(
            'Kategori Referansi',
            size=64,
            required=False),
        'custom_products':fields.boolean('Custom Products')
    }
product_category()