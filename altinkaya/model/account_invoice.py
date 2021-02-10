from openerp.osv import osv, fields
from werkzeug import url_encode
import hashlib

class account_invoice(osv.Model):
    _inherit = 'account.invoice'
    _order = 'id desc'

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


    
    def invoice_validate(self, cr, uid, ids, context=None):
        res = super(account_invoice, self).invoice_validate(cr, uid, ids, context=context)
        
        user = self.pool.get('res.users').browse(cr,uid,[uid],context=context)
        for invoice in self.pool.get('account.invoice').browse(cr,uid, ids, context=context):
            for picking in invoice.picking_ids:
                if picking.carrier_id.id != invoice.carrier_id.id:
                    picking.message_post(body='Carrier changed from %s to %s through invoice by %s' % (picking.carrier_id.name,invoice.carrier_id.name, user.name))
                    picking.write({'carrier_id':invoice.carrier_id.id})
        
        return res

    def _amount8_untaxed(self, cr, uid, ids, field, arg, context=None):
        res = dict.fromkeys(ids, False)
        for invoice in self.browse(cr, uid, ids, context=context):
            amount = 0.0
            for tax in invoice.tax_line:
                if tax.name == u'KDV %8':
                    amount = amount + tax.base
            res[invoice.id] = amount
        return res

    def _amount18_untaxed(self, cr, uid, ids, field, arg, context=None):
        res = dict.fromkeys(ids, False)
        for invoice in self.browse(cr, uid, ids, context=context):
            amount = 0.0
            for tax in invoice.tax_line:
                if tax.name == u'KDV %18':
                    amount = amount + tax.base
            res[invoice.id] = amount
        return res


    def _amount8_tax(self, cr, uid, ids, field, arg, context=None):
        res = dict.fromkeys(ids, False)
        for invoice in self.browse(cr, uid, ids, context=context):
            amount = 0.0
            for tax in invoice.tax_line:
                if tax.name == u'KDV %8':
                    amount = amount + tax.amount
            res[invoice.id] = amount
        return res

    def _amount18_tax(self, cr, uid, ids, field, arg, context=None):
        res = dict.fromkeys(ids, False)
        for invoice in self.browse(cr, uid, ids, context=context):
            amount = 0.0
            for tax in invoice.tax_line:
                if tax.name == u'KDV %18':
                    amount = amount + tax.amount
            res[invoice.id] = amount
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
        'amount8_untaxed': fields.function(_amount8_untaxed, type='float', string='Amount 8 untaxed',readonly=True, store=False),
        'amount18_untaxed': fields.function(_amount18_untaxed, type='float', string='Amount 18 untaxed',readonly=True, store=False),
        'amount18_tax': fields.function(_amount18_tax, type='float', string='Amount 18 tax',readonly=True, store=False),
        'amount8_tax': fields.function(_amount8_tax, type='float', string='Amount 8 tax',readonly=True, store=False),
    }


account_invoice()