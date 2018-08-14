#from openerp.osv import osv, fields
from openerp.tools.translate import _

from openerp import models,fields, api

from werkzeug import url_encode
import hashlib

class sale_order(models.Model):
    _inherit = 'sale.order'


    altinkaya_payment_url = fields.Char(string='Altinkaya Payment Url',compute='_altinkaya_payment_url')
    contains_set_product = fields.Boolean('Contains set products',compute='_contains_set_products')
    
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
        
    @api.one
    @api.depends('order_line.set_product')
    def _contains_set_products(self):
        self.contains_set_product = any(self.order_line.filtered(lambda l: l.set_product == True))
    
    
    
    @api.multi
    def action_explode_set_products(self):
        self.ensure_one()
        for line in self.order_line.filtered(lambda l: l.set_product == True):
            line.explode_set_contents()


class sale_order_line(models.Model):
    _inherit= 'sale.order.line'
    
    show_custom_products = fields.Boolean('Show Custom Products')
    set_product = fields.Boolean('Set product?', compute='_compute_set_product')
    
    @api.one
    @api.depends('product_id')
    def _compute_set_product(self):
        bom_obj = self.env['mrp.bom'].sudo()
        bom_id = bom_obj._bom_find(product_id=self.product_id.id, properties=self.property_ids)
        if not bom_id:
            self.set_product = False
        else:
            bom_id = bom_obj.browse(bom_id)
            self.set_product = bom_id.type == 'phantom'
        
    
    @api.onchange('show_custom_products')
    def onchange_show_custom(self):
        domain = []
        self.product_tmpl_id = False
        self.product_id = False
        
        if not self.show_custom_products:
            custom_categories = self.env['product.category'].search([('custom_products','=',True)])
            domain = [('categ_id','not in',custom_categories.ids)]
            
        return {'domain':{'product_tmpl_id':domain}}
    
    
    
    @api.multi
    def explode_set_contents(self):
        """ Explodes order lines.
        """
        self.ensure_one()
        bom_obj = self.env['mrp.bom'].sudo()
        prod_obj = self.env["product.product"].sudo()
        uom_obj = self.env["product.uom"].sudo()
        
        to_explode_again_ids = []
        property_ids = self.property_ids
        bom_id = bom_obj._bom_find(product_id=self.product_id.id, properties=property_ids)
        if not bom_id:
            return
        
        bom_id = bom_obj.browse(bom_id)
        if bom_id.type == 'phantom':
            factor = uom_obj._compute_qty(self.product_uom.id, self.product_uom_qty, bom_id.product_uom.id) / bom_id.product_qty
            res = bom_id._bom_explode(self.product_id, factor, property_ids)

            for line in res[0]:
                product = prod_obj.browse( line['product_id'])
                if product.type != 'service':
                    valdef = {
                        'order_id': self.order_id.id,
                        'product_id': line['product_id'],
                        'product_uom': line['product_uom'],
                        'product_uom_qty': line['product_qty'],
#                        'product_uos': line['product_uos'],
#                        'product_uos_qty': line['product_uos_qty'],
                        'name': line['name'],
                    }
                    sol_id = self.create(valdef)
                    to_explode_again_ids.append(sol_id)
            
            #check if new moves needs to be exploded
            if to_explode_again_ids:
                for sol in to_explode_again_ids:
                    sol.explode_set_contents()
            
            #delete the line with original product which is not relevant anymore
            self.unlink()
            

    
    