from openerp.osv import osv, fields


class account_invoice(osv.Model):
    _inherit = 'account.invoice'
    _columns = {
        'x_serino': fields.char(
            'Fatura No',
            size=64,
            required=False,
            select=1),
        'x_teslimat': fields.char(
            'Teslimat Kisaltmasi',
            size=64,
            required=False),
        'address_contact_id': fields.many2one(
            'res.partner',
            'Shipping Address'

            ),
                }

account_invoice()