from openerp.osv import osv, fields


class account_voucher(osv.Model):
    _inherit = 'account.voucher'
    _columns = {
        'x_cek_vergi': fields.char(
            'Cek Vergi No',
            size=64,
            required=False,
            select=1),
        'x_cek_tarih': fields.date(
            'Keside Tarihi',
            help="Cekin Vade Tarihi"),
        'x_cek_no': fields.char(
            'Cek No',
            size=64,
            required=False),
        'x_cek_banka': fields.char(
            'Cek banka Adi',
            size=64,
            required=False),
    }
account_voucher()
