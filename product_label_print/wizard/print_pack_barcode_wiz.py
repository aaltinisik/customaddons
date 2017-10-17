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
#            product_label_id = product_label_obj.search([('product_id','=',product)], limit=1)
#            if not product_label_id:
            product_id = self.env['product.product'].browse(product)
            
            product_label_id = product_label_obj.create({
                    'name': product_id.name,
                    'default_code': product_id.default_code,
                    'short_code': product_id.default_code,
                    'note': product_id.description,
                    'pieces_in_pack': product_id.pieces_in_pack,
                    'label_to_print': 1,
                    'barcode': product_id.ean13,
                    'product_id': product_id.id
            })
            product_ids.append(product_label_id.id)
        res.update({'product_label_ids': [(6, 0, product_ids)] or []})
        return res

    @api.multi
    def show_label(self):
        datas = {
                'ids': self.env.context.get('active_ids'),
                'model': 'print.pack.barcode.wiz'
            }
        res = {
            'type' : 'ir.actions.report.xml',
            'report_name': 'product_label_print',
            'datas' : datas,
        }
        return self.env['report'].get_action(self, 'product_label_print')


    @api.multi
    def print_label(self):
        cr  = self.env.cr
        uid = self.env.uid
        ids = self.ids
        context = self.env.context

        server_action_ids = [1142]
        server_action_ids = map(int, server_action_ids)
        action_server_obj = self.pool.get('ir.actions.server')
        ctx = dict(context, active_model='print.pack.barcode.wiz', active_ids=ids, active_id=ids[0])
        action_server_obj.run(cr, uid, server_action_ids, context=ctx)

        return {'type': 'ir.actions.act_window_close'}