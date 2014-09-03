from openerp.osv import osv, fields
from openerp.tools.translate import _

from werkzeug import url_encode
import hashlib

class sale_order(osv.Model):
    _inherit = 'sale.order'

    def _altinkaya_payment_url(self, cr, uid, ids, field, arg, context=None):
        res = dict.fromkeys(ids, False)
        for order in self.browse(cr, uid, ids, context=context):

            tutar = '%d' % (int)(100*order.amount_total)
            eposta = order.partner_id.email
            if eposta is False:
                eposta = ""
            params = {
                    "email": unicode(eposta),
                    "musteri": unicode(order.partner_id.commercial_partner_id.name),
                    "oid": unicode(order.name),
                    "tutar": unicode(tutar),
                    "ref": unicode(order.partner_id.commercial_partner_id.ref),
                    "currency": unicode(order.currency_id.name),
                    "lang": unicode(order.partner_id.lang),
                    "hashtr": hashlib.sha1(unicode(order.currency_id.name) + unicode(order.partner_id.commercial_partner_id.ref) + unicode(eposta) + unicode(tutar) + unicode(order.name) + unicode(order.company_id.hash_code)).hexdigest().upper(),
                    }
            res[order.id] = "https://www.altinkaya.eu/payment/paymentform.php?" + url_encode(params)
        return res

    _columns = {
                'altinkaya_payment_url': fields.function(_altinkaya_payment_url, type='char', string='Altinkaya Payment Url'),
                }

sale_order()

