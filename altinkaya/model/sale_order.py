from openerp.osv import osv, fields
from openerp.tools.translate import _

from werkzeug import url_encode
import hashlib

class sale_order(osv.Model):
    _inherit = 'sale.order'

    def print_quotation(self, cr, uid, ids, context=None):
        '''
        This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        self.signal_workflow(cr, uid, ids, 'quotation_sent')
        return self.pool['report'].get_action(cr, uid, ids, 'sale.orderprint', context=context)


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
            res[order.id] = "?" + url_encode(params)
        return res

    _columns = {
                'altinkaya_payment_url': fields.function(_altinkaya_payment_url, type='char', string='Altinkaya Payment Url'),
                }

sale_order()

