# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from werkzeug import url_encode
import hashlib


def _match_production_with_route(production):
    ongoing_state = ['planned', 'progress']
    production_ids = production.sorted(key=lambda m: m.id)
    if production_ids:
        process_ids = production_ids.mapped('process_id.id')
        if 14 in process_ids:
            if any(production_ids.filtered(lambda r: r.process_id.id == 14 and r.state in ongoing_state)):
                return 'molding'
            else:
                return 'molding_waiting'
        elif any(x in [1, 11] for x in process_ids):
            if any(production_ids.filtered(lambda r: r.process_id.id in [1, 11] and r.state in ongoing_state)):
                return 'injection'
            else:
                return 'injection_waiting'
        elif 2 in process_ids:
            if any(production_ids.filtered(lambda r: r.process_id.id == 2 and r.state in ongoing_state)):
                return 'cnc'
            else:
                return 'cnc_waiting'
        elif 10 in process_ids:
            if any(production_ids.filtered(lambda r: r.process_id.id == 10 and r.state in ongoing_state)):
                return 'metal'
            else:
                return 'metal_waiting'
        elif 5 in process_ids:
            if any(production_ids.filtered(lambda r: r.process_id.id == 5 and r.state in ongoing_state)):
                return 'cnc_lathe'
            else:
                return 'cnc_lathe_waiting'
        elif 16 in process_ids:
            if any(production_ids.filtered(lambda r: r.process_id.id == 16 and r.state in ongoing_state)):
                return 'uv_printing'
            else:
                return 'uv_printing_waiting'
        elif any(x in [3, 6, 7] for x in process_ids):
            if any(production_ids.filtered(lambda r: r.process_id.id in [3, 6, 7] and r.state in ongoing_state)):
                return 'assembly'
            else:
                return 'assembly_waiting'
    else:
        return 'at_warehouse'


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    production_ids = fields.One2many(string='Productions', comodel_name='mrp.production',
                                     inverse_name='sale_id')
    order_state = fields.Selection([
        ('draft', 'Taslak'),
        ('sent', 'Teklif Gönderildi'),
        ('sale', 'Satış Siparişi'),
        ('molding_waiting', 'Kalıphanede Bekliyor'),
        ('molding', 'Kalıphanede'),
        ('injection_waiting', 'Enjeksiyonda Bekliyor'),
        ('injection', 'Enjeksiyonda'),
        ('metal_waiting', 'Preshane Bekliyor'),
        ('metal', 'Preshane'),
        ('cnc_lathe_waiting', 'CNC Torna Bekliyor'),
        ('cnc_lathe', 'CNC Torna'),
        ('cnc_waiting', 'CNC Bekliyor'),
        ('cnc', 'CNC Kesimde'),
        ('uv_printing_waiting', 'Görsel Baskıda Bekliyor'),
        ('uv_printing', 'Görsel Baskıda'),
        ('assembly_waiting', 'Montajda Bekliyor'),
        ('assembly', 'Montajda'),
        ('at_warehouse', 'Depoda'),
        ('on_transit', 'Nakliyede'),
        ('delivered', 'Teslim Edildi'),
        ('completed', 'Tamamlandı'),
        ('cancel', 'İptal')], string='Sipariş Durumu', readonly=True, copy=False, default='draft',
        index=True, track_visibility='onchange', compute="_compute_order_state", track_sequence=3, store=True)

    @api.multi
    @api.depends('state',
                 'picking_ids.state',
                 'production_ids.state',
                 'picking_ids.delivery_state',
                 'picking_ids.invoice_state')
    def _compute_order_state(self):
        deadline = datetime.now() - timedelta(days=360)
        for sale in self:
            # SALE
            if sale.confirmation_date and sale.confirmation_date < deadline:
                sale.order_state = 'completed'
                pass
            elif sale.state == 'draft':
                sale.order_state = 'draft'
            elif sale.state == 'sent':
                sale.order_state = 'sent'
            elif sale.state == 'sale':
                sale.order_state = 'sale'
            elif sale.state == 'cancel':
                sale.order_state = 'cancel'
                continue
            else:
                pass
            # PRODUCTION
            ongoing_productions = sale.production_ids.filtered(lambda p: p.state in ['confirmed', 'planned',
                                                                                     'progress'])
            if ongoing_productions:
                sale.order_state = _match_production_with_route(ongoing_productions)
            # PICKING
            elif sale.picking_ids:
                outgoing_pickings = sale.picking_ids.filtered(lambda p:
                                                              p.picking_type_code == 'outgoing' and
                                                              p.state == 'done' and
                                                              p.invoice_state == 'invoiced')
                if outgoing_pickings:
                    if any(p.delivery_state == 'customer_delivered' for p in outgoing_pickings):
                        sale.order_state = 'delivered'
                    else:
                        sale.order_state = 'on_transit'
                else:
                    sale.order_state = 'at_warehouse'
        return True

    altinkaya_payment_url = fields.Char(string='Altinkaya Payment Url', compute='_altinkaya_payment_url')
    sale_line_history = fields.One2many('sale.order.line', string="Old Sales", compute="_compute_sale_line_history")
    sale_currency_rate = fields.Float(string="Currency Rate", compute="_compute_sale_currency_rate", default=1.0,
                                      digits=[16, 4])

    @api.multi
    @api.depends('currency_id', 'date_order')
    def _compute_sale_currency_rate(self):
        currency_id = self.currency_id or self.env.user.company_id.currency_id
        if self.partner_id and self.partner_id.use_second_rate_type:
            curr_dict = currency_id.with_context(use_second_rate_type=True)._get_rates(self.env.user.company_id, self.date_order)
        else:
            curr_dict = currency_id._get_rates(self.env.user.company_id, self.date_order)
        self.sale_currency_rate = 1 / curr_dict.get(currency_id.id, 1.0)
        return True

    @api.multi
    def action_quotation_send(self):
        res = super(SaleOrder, self).action_quotation_send()

        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('altinkaya_sales', 'email_template_edi_sale_altinkaya')[1]
        except ValueError:
            template_id = False

        context = res.get("context", {})
        context.update({
            "default_template_id": template_id
        })

        res.update({"context": context})
        return res

    def _compute_sale_line_history(self):

        for sale in self:
            last_sale_lines = sale.env['sale.order.line'].search(
                [('order_id.partner_id', '=', sale.partner_id.id), ('state', 'not in', ['draft', 'sent', 'cancelled'])],
                limit=50, order="id desc")
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
            tutar = '%d' % (int)(100 * order.amount_total)
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
                "hashtr": hashlib.sha1((
                        order.currency_id.name + order.partner_id.commercial_partner_id.ref + eposta + tutar + order.name + order.company_id.hash_code).encode(
                    'utf-8')).hexdigest().upper(),
            }
            order.altinkaya_payment_url = "?" + url_encode(params)

    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        for sale in self:
            sale.order_line.explode_set_contents()
        return res

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        res.order_line.explode_set_contents()
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    show_custom_products = fields.Boolean('Show Custom Products')
    set_product = fields.Boolean('Set product?', compute='_compute_set_product')
    date_order = fields.Datetime(related="order_id.date_order")

    def copy_line_to_active_order(self):
        sale = self.env['sale.order'].browse(
            self.env.context.get('active_order_id') or self.env.context.get('params', {}).get('id'))
        for line in self:
            sale.write({'order_line': [(0, 0, {
                'name': line.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty, })]})

            sale.order_line._compute_amount()

    @api.one
    @api.depends('product_id')
    def _compute_set_product(self):
        bom_obj = self.env['mrp.bom'].sudo()
        bom_id = bom_obj._bom_find(product=self.product_id)
        if not bom_id:
            self.set_product = False
        else:
            # bom_id = bom_obj.browse(bom_id.id)
            self.set_product = bom_id.type == 'phantom'

    @api.onchange('show_custom_products')
    def onchange_show_custom(self):
        domain = [('sale_ok', '=', True)]
        self.product_tmpl_id = False
        self.product_id = False

        if not self.show_custom_products:
            custom_categories = self.env['product.category'].search([('custom_products', '=', True)])
            domain = ['&', ('sale_ok', '=', True), ('categ_id', 'not in', custom_categories.ids)]

        return {'domain': {'product_tmpl_id': domain}}

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
            customer_lang = line.order_id.partner_id.lang
            if not bom_id:
                continue
            # bom_id = bom_obj.browse(bom_id)
            if bom_id.type == 'phantom':
                factor = line.product_uom._compute_quantity(line.product_qty,
                                                            bom_id.product_uom_id) / bom_id.product_qty
                boms, lines = bom_id.explode(line.product_id, factor,
                                             picking_type=bom_id.picking_type_id)

                for bom_line, data in lines:
                    sol = self.env['sale.order.line'].new()
                    sol.order_id = line.order_id
                    sol.product_id = bom_line.product_id
                    sol.product_uom_qty = data['qty']  # data['qty']
                    sol.product_id_change()
                    sol.product_uom_change()
                    sol._onchange_discount()
                    sol._compute_amount()
                    sol.name = bom_line.product_id.with_context({'lang': customer_lang}).display_name
                    vals = sol._convert_to_write(sol._cache)

                    sol_id = self.create(vals)
                    to_explode_again_ids |= sol_id

                to_unlink_ids |= line

        # check if new moves needs to be exploded
        if to_explode_again_ids:
            to_explode_again_ids.explode_set_contents()
        # delete the line with original product which is not relevant anymore
        if to_unlink_ids:
            to_unlink_ids.unlink()
