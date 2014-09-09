from openerp.osv import osv, fields
from werkzeug import url_encode
import hashlib

class account_invoice(osv.Model):
    _inherit = 'account.invoice'

    def _altinkaya_payment_url(self, cr, uid, ids, field, arg, context=None):
        res = dict.fromkeys(ids, False)
        for invoice in self.browse(cr, uid, ids, context=context):

            tutar = '%d' % (int)(100*invoice.amount_total)
            eposta = invoice.partner_id.email
            if eposta is False:
                eposta = ""
            params = {
                    "email": unicode(eposta),
                    "musteri": unicode(invoice.partner_id.commercial_partner_id.name),
                    "oid": unicode(invoice.number),
                    "tutar": unicode(tutar),
                    "ref": unicode(invoice.partner_id.commercial_partner_id.ref),
                    "currency": unicode(invoice.currency_id.name),
                    "lang": unicode(invoice.partner_id.lang),
                    "hashtr": hashlib.sha1(unicode(invoice.currency_id.name) + unicode(invoice.partner_id.commercial_partner_id.ref) + unicode(eposta) + unicode(tutar) + unicode(invoice.number) + unicode(invoice.company_id.hash_code)).hexdigest().upper(),
                    }
            res[invoice.id] = "?" + url_encode(params)
        return res




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
        'altinkaya_payment_url': fields.function(_altinkaya_payment_url, type='char', string='Altinkaya Payment Url'),
                }

account_invoice()