# coding: utf-8

from openerp import api, fields, models, _


class print_pack_barcode_wiz(models.TransientModel):
    _name = 'print.pack.barcode.wiz'
    _description = 'Product Label Print'

    product_ids = fields.Many2many('product.product', string="Products")

    @api.model
    def default_get(self, fields):
        ''' 
        To get default values for the object.
        '''
        res = super(print_pack_barcode_wiz, self).default_get(fields)
        res.update({'product_ids': [(6, 0, self.env.context.get('active_ids'))] or []})
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