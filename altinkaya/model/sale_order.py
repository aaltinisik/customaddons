# from openerp.osv import osv, fields
from openerp.tools.translate import _

from openerp import models, fields, api

from werkzeug import url_encode
import hashlib


class sale_order(models.Model):
    _inherit = 'sale.order'

    altinkaya_payment_url = fields.Char(string='Altinkaya Payment Url', compute='_altinkaya_payment_url')

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
            tutar = '%d' % (int)(100 * order.amount_total)
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
                "hashtr": hashlib.sha1(
                    unicode(order.currency_id.name) + unicode(order.partner_id.commercial_partner_id.ref) + unicode(
                        eposta) + unicode(tutar) + unicode(order.name) + unicode(
                        order.company_id.hash_code)).hexdigest().upper(),
            }
            order.altinkaya_payment_url = "?" + url_encode(params)

    @api.multi
    def write(self, vals):
        res = super(sale_order, self).write(vals)
        self.order_line.explode_set_contents()
        return res

    @api.model
    def create(self, vals):
        res = super(sale_order, self).create(vals)
        res.order_line.explode_set_contents()
        return res


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

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
            custom_categories = self.env['product.category'].search([('custom_products', '=', True)])
            domain = [('categ_id', 'not in', custom_categories.ids)]

        return {'domain': {'product_tmpl_id': domain}}

    @api.multi
    def explode_set_contents(self):
        """ Explodes order lines.
        """

        bom_obj = self.env['mrp.bom'].sudo()
        prod_obj = self.env["product.product"].sudo()
        uom_obj = self.env["product.uom"].sudo()
        to_unlink_ids = self.env['sale.order.line']
        to_explode_again_ids = self.env['sale.order.line']

        for line in self.filtered(lambda l: l.set_product == True and l.state in ['draft', 'sent']):
            property_ids = line.property_ids
            bom_id = bom_obj._bom_find(product_id=line.product_id.id, properties=property_ids)
            if not bom_id:
                continue
            bom_id = bom_obj.browse(bom_id)
            if bom_id.type == 'phantom':
                factor = uom_obj._compute_qty(line.product_uom.id, line.product_uom_qty,
                                              bom_id.product_uom.id) / bom_id.product_qty
                res = bom_id._bom_explode(line.product_id, factor, property_ids)

                for bom_line in res[0]:
                    product = prod_obj.browse(bom_line['product_id'])

                    res = self.env['sale.order.line'].product_id_change(
                        line.order_id.pricelist_id.id, product.id,
                        qty=bom_line['product_qty'], uom=bom_line['product_uom'],
                        qty_uos=bom_line['product_qty'], uos=bom_line['product_uom'],
                        name=bom_line['name'], partner_id=line.order_id.partner_id.id, lang=False,
                        update_tax=True, date_order=line.order_id.date_order, packaging=False,
                        fiscal_position=line.order_id.fiscal_position.id, flag=False)

                    valdef = res['value']

                    valdef.update({
                        'order_id': line.order_id.id,
                        'product_id': product.id,
                        'product_tmpl_id': product.product_tmpl_id.id,
                        'product_uom': bom_line['product_uom'],
                        'product_uom_qty': bom_line['product_qty'],
                        #                        'product_uos': line['product_uos'],
                        #                        'product_uos_qty': line['product_uos_qty'],
                        'name': bom_line['name'],
                        #                        'discount':line.discount,
                        'tax_id': [(4, tax_id, False) for tax_id in valdef['tax_id']]
                    })

                    sol_id = self.create(valdef)
                    to_explode_again_ids |= sol_id

                to_unlink_ids |= line

        # check if new moves needs to be exploded
        if to_explode_again_ids:
            to_explode_again_ids.explode_set_contents()
            # delete the line with original product which is not relevant anymore
        if to_unlink_ids:
            to_unlink_ids.unlink()



