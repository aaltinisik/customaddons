# coding: utf-8

from openerp import api, fields, models, _


class print_pack_barcode_wiz(models.TransientModel):
    _name = 'print.pack.barcode.wiz'
    _description = 'Product Label Print'

    # product_ids = fields.Many2many('product.product', string="Products")
    product_label_ids = fields.Many2many('product.product.label', string="Products")

    @api.model
    def default_get(self, fields):
        ''' 
        To get default values for the object.
        '''
        product_label_obj = self.env['product.product.label']
        res = super(print_pack_barcode_wiz, self).default_get(fields)
        product_ids = []
        for product in self.env.context.get('active_ids'):
            product_label_id = product_label_obj.search([('product_id','=',product)], limit=1)
            if not product_label_id:
                product_id = self.env['product.product'].browse(product)
                product_label_id = product_label_obj.create({
                        'name': product_id.name,
                        'default_code': product_id.default_code,
                        'note': product_id.description,
                        'pieces_in_pack': product_id.pieces_in_pack,
                        'label_to_print': 1,
                        'product_id': product_id.id
                    })
            product_ids.append(product_label_id.id)
        res.update({'product_label_ids': [(6, 0, product_ids)] or []})
        return res

    # @api.multi
    # def print_label(self):
    #     print "\n\n CALL print_label"


    @api.multi
    def print_label(self):
        datas = {
                'ids': self.env.context.get('active_ids'),
                'model': 'product.product'
            }
        res = {
            'type' : 'ir.actions.report.xml',
            'report_name': 'Print Product Label',
            'datas' : datas,
        }
        # return self.env['report'].get_action(self, 'product_label_print.aeroo_product_label_print_id')
        return res