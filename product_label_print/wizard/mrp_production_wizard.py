# coding: utf-8

from openerp import api, fields, models, _


class mrp_production_product_wizard(models.TransientModel):
    _name = 'mrp.production.product.wizard'
    _description = 'Product Label Print'

    product_label_ids = fields.Many2many('product.product.label', string="Products")
    label_ids = fields.Many2many('label.twoinrow', string="Labels")
    skip_first = fields.Boolean('Skip First Label')

    @api.model
    def default_get(self, fields_list):
        product_list = []
        res = super(mrp_production_product_wizard, self).default_get(fields_list)
        product_label_obj = self.env['product.product.label']
        if self._context.get('active_ids'):
            for each_mrp in self.env['mrp.production'].browse(self._context.get('active_ids')):
                no_of_product = len(each_mrp.move_lines)
                for each_move in each_mrp.move_lines:
                    pieces_in_pack = round(no_of_product / each_move.product_id.product_tmpl_id.pieces_in_pack) if each_move.product_id.product_tmpl_id.pieces_in_pack > 0 else 1
                    product_label_id = product_label_obj.create({'product_id': each_move.product_id.id,
                                                'note': each_move.product_id.product_tmpl_id.description,
                                                'name':each_move.product_id.product_tmpl_id.name,
                                                'default_code':each_move.product_id.default_code,
                                                'barcode':each_move.product_id.ean13,
                                                'pieces_in_pack':each_move.product_id.product_tmpl_id.pieces_in_pack,
                                                'no_of_products':no_of_product,
                                                'label_to_print':pieces_in_pack if pieces_in_pack > 0 else 1
                                                })
                    product_list.append(product_label_id.id)
            res.update({'product_label_ids': [(6, 0, product_list)]})
        return res

    @api.multi
    def print_label(self):
        cr = self.env.cr
        uid = self.env.uid
        ids = self.ids
        context = self.env.context
        self.generate_labels()

        server_action_ids = [1143]
        server_action_ids = map(int, server_action_ids)
        action_server_obj = self.pool.get('ir.actions.server')
        ctx = dict(context, active_model='mrp.production.product.wizard', active_ids=ids, active_id=ids[0])
        action_server_obj.run(cr, uid, server_action_ids, context=ctx)

        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def show_label(self):
        self.generate_labels()
        datas = {
                'ids': self.env.context.get('active_ids'),
                'model': 'mrp.production.product.wizard'
            }
        res = {
            'type' : 'ir.actions.report.xml',
            'report_name': 'mrp_product_label_print',
            'datas' : datas,
        }
        return self.env['report'].get_action(self, 'mrp_product_label_print')

    @api.multi
    def generate_labels(self):
        last_label = self.product_label_ids[0]
        leap_label = False
        Label_Res = []
        label_template_obj = self.env['label.twoinrow']
        for product_label in self.product_label_ids:
            labels_to_print = product_label.label_to_print
            while labels_to_print > 0:
                if self.skip_first:
                    Label_l = label_template_obj.create({
                        'first_label_empty' : True,
                        'label1': product_label.id,
                        'second_label_empty': False,
                        'label2': product_label.id,
                        'copies_to_print': 1,
                    })
                    Label_Res.append(Label_l.id)
                    self.skip_first = False
                    labels_to_print = labels_to_print - 1
                if leap_label:
                    Label_l = label_template_obj.create({
                        'first_label_empty': False,
                        'label1': last_label.id,
                        'second_label_empty': False,
                        'label2': product_label.id,
                        'copies_to_print': 1,
                    })
                    Label_Res.append(Label_l.id)
                    leap_label = False
                    labels_to_print = labels_to_print - 1

                if labels_to_print > 1:
                    # 1 1
                    Label_l = label_template_obj.create({
                        'first_label_empty': False,
                        'label1': product_label.id,
                        'second_label_empty': False,
                        'label2': product_label.id,
                        'copies_to_print': labels_to_print / 2,
                    })
                    labels_to_print = labels_to_print - ((labels_to_print / 2) * 2)
                    Label_Res.append(Label_l.id)
                if labels_to_print == 1:
                    leap_label = True
                    last_label = product_label
                    labels_to_print = 0
        if leap_label:
            Label_l = label_template_obj.create({
                # Tek last label
                'first_label_empty': False,
                'label1': product_label.id,
                'second_label_empty': True,
                'label2': product_label.id,
                'copies_to_print': 1,
                })
            Label_Res.append(Label_l.id)
        self.label_ids = [(6, 0, Label_Res)]
        return False
