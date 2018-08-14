#from openerp.osv import osv, fields
from openerp.tools.translate import _

from openerp import models,fields, api

from werkzeug import url_encode
import hashlib

class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def print_quotation(self):
        '''
        This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(self.ids) == 1, 'This option should only be used for a single id at a time'
        self.signal_workflow('quotation_sent')
        return self.env['report'].get_action(self, 'sale.orderprint')

    @api.multi
    def _altinkaya_payment_url(self):
        for order in self:
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
            order.altinkaya_payment_url = "?" + url_encode(params)
        
    altinkaya_payment_url = fields.Char(string='Altinkaya Payment Url',compute='_altinkaya_payment_url')
    




class sale_order_line(models.Model):
    _inherit= 'sale.order.line'
    
    show_custom_products = fields.Boolean('Show Custom Products')
    
    @api.onchange('show_custom_products')
    def onchange_show_custom(self):
        domain = []
        self.product_tmpl_id = False
        self.product_id = False
        
        if not self.show_custom_products:
            custom_categories = self.env['product.category'].search([('custom_products','=',True)])
            domain = [('categ_id','not in',custom_categories.ids)]
            
        return {'domain':{'product_tmpl_id':domain}}
    