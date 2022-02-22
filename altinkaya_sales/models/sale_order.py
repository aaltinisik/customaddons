# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _
from werkzeug import url_encode
import hashlib

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
    production_ids = fields.Many2many('mrp.production',string='Manufacturing Orders', compute='_compute_productions')
    
    @api.multi
    def _compute_productions(self):
        for so in self:
            so.production_ids = self.env['mrp.production'].search([('sale_id','=', so.id)])
            
            
    
    altinkaya_payment_url = fields.Char(string='Altinkaya Payment Url',compute='_altinkaya_payment_url')
    
    sale_line_history = fields.One2many('sale.order.line',string="Old Sales",compute="_compute_sale_line_history")
    
    @api.multi
    def action_quotation_send(self):
        res = super(SaleOrder,self).action_quotation_send()
        
        
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('altinkaya_sales', 'email_template_edi_sale_altinkaya')[1]
        except ValueError:
            template_id = False
        
        context = res.get("context",{})
        context.update({
            "default_template_id":template_id
            })
        
        res.update({"context":context})
        return res
    
    
    def _compute_sale_line_history(self):
        
        for sale in self:
            last_sale_lines = sale.env['sale.order.line'].search([('order_id.partner_id','=',sale.partner_id.id),('state','not in',['draft','sent','cancelled'])],limit=50,order="id desc")
            sale.sale_line_history = last_sale_lines.ids
    
#     @api.multi
#     def print_quotation(self):
#         '''
#         This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
#         '''
#         assert len(self.ids) == 1, 'This option should only be used for a single id at a time'
#         self.signal_workflow('quotation_sent')
#         return self.env['report'].get_action(self, 'sale.orderprint')

    @api.multi
    def _altinkaya_payment_url(self):
        for order in self:
            tutar = '%d' % (int)(100*order.amount_total)
            eposta = order.partner_id.email
            if eposta is False:
                eposta = ""
            params = {
                    "email": eposta,
                    "musteri": order.partner_id.commercial_partner_id.name,
                    "oid": order.name,
                    "tutar": tutar,
                    "ref": order.partner_id.commercial_partner_id.ref,
                    "currency": order.currency_id.name,
                    "lang": order.partner_id.lang,
                    "hashtr": hashlib.sha1((order.currency_id.name + order.partner_id.commercial_partner_id.ref + eposta + tutar + order.name + order.company_id.hash_code).encode('utf-8')).hexdigest().upper(),
                    }
            order.altinkaya_payment_url = "?" + url_encode(params)

    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        self.order_line.explode_set_contents()
        return res

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        res.order_line.explode_set_contents()
        return res

    


class sale_order_line(models.Model):
    _inherit= 'sale.order.line'
    
    show_custom_products = fields.Boolean('Show Custom Products')
    set_product = fields.Boolean('Set product?', compute='_compute_set_product')
    date_order = fields.Datetime(related="order_id.date_order")  
    
    
    def copy_line_to_active_order(self):
        sale = self.env['sale.order'].browse(self.env.context.get('active_order_id') or  self.env.context.get('params',{}).get('id'))
        for line in self:
        
            sale.write({'order_line':[(0,0,{
                'name':line.name,
                'product_id':line.product_id.id,
                'product_uom_qty':line.product_uom_qty,})]})
            
            sale.order_line._compute_amount()
    
       
    @api.one
    @api.depends('product_id')
    def _compute_set_product(self):
        bom_obj = self.env['mrp.bom'].sudo()
        bom_id = bom_obj._bom_find(product=self.product_id)
        if not bom_id:
            self.set_product = False
        else:
            #bom_id = bom_obj.browse(bom_id.id)
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

        bom_obj = self.env['mrp.bom'].sudo()
        prod_obj = self.env["product.product"].sudo()
        uom_obj = self.env["uom.uom"].sudo()
        to_unlink_ids = self.env['sale.order.line']
        to_explode_again_ids = self.env['sale.order.line']

        for line in self.filtered(lambda l: l.set_product == True and l.state in ['draft', 'sent']):
            bom_id = bom_obj._bom_find(product=line.product_id)
            if not bom_id:
                continue
            #bom_id = bom_obj.browse(bom_id)
            if bom_id.type == 'phantom':
                factor = line.product_uom._compute_quantity(line.product_qty,
                                                                     bom_id.product_uom_id) / bom_id.product_qty
                boms, lines = bom_id.explode(line.product_id, factor,
                                                        picking_type=bom_id.picking_type_id)

                for bom_line, data in lines:
                    sol = self.env['sale.order.line'].new()
                    sol.order_id = line.order_id
                    sol.product_id = bom_line.product_id
                    sol.product_uom_qty = data['qty']    #data['qty']
                    sol.product_id_change()
                    sol.product_uom_change()
                    sol._onchange_discount()
                    sol._compute_amount()
                    vals = sol._convert_to_write(sol._cache)

                    sol_id = self.create(vals)
                    to_explode_again_ids |= sol_id

                to_unlink_ids |= line

        #check if new moves needs to be exploded
        if to_explode_again_ids:
            to_explode_again_ids.explode_set_contents()
        #delete the line with original product which is not relevant anymore
        if to_unlink_ids:
            to_unlink_ids.unlink()