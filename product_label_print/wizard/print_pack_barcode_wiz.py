# coding: utf-8

from odoo import api, fields, models, _
from odoo.exceptions import Warning, UserError


class PrintPackBarcodeWizard(models.TransientModel):
    _name = 'print.pack.barcode.wiz'
    _description = 'Product Label Print'
    
    product_label_ids = fields.Many2many('product.product.label', string="Products")
    label_ids = fields.Many2many('label.twoinrow', string="Labels")
    skip_first = fields.Boolean('Skip First Label')
    restrict_single = fields.Boolean('Restrict to single product', default=False)
    single_label_id = fields.Many2one('product.product.label',compute='_compute_single_label')
    single_label_name = fields.Char(string="Name",related='single_label_id.name')
    single_label_nameL1 = fields.Char(string="NameL1",related='single_label_id.nameL1')
    single_label_nameL2 = fields.Char(string="NameL1",related='single_label_id.nameL2')
    single_label_nameL3 = fields.Char(string="NameL2",related='single_label_id.nameL3')
    single_label_nameL4 = fields.Char(string="NameL3",related='single_label_id.nameL4')
    single_label_default_code = fields.Char(string="Default Code",related='single_label_id.default_code')
    single_label_short_code = fields.Char(string="Short Code",related='single_label_id.short_code')
    single_label_product_id = fields.Many2one('product.product', string="Product", related='single_label_id.product_id')
    single_label_barcode = fields.Char(string="Barcode", related='single_label_id.barcode')
    single_label_uom_name = fields.Char(string="UOM Name", related='single_label_id.uom_name')
    single_label_note = fields.Char(string="Note",related='single_label_id.note', readonly=False)
    single_label_pieces_in_pack = fields.Float(string="# in Cartoon", related='single_label_id.pieces_in_pack', readonly=False)
    single_label_label_to_print = fields.Integer(string='# of label to be printed', related='single_label_id.label_to_print', readonly=False)
    printer_type = fields.Char(string='User Printer Type', compute='_get_user_printer_type', store=False)

    @api.one
    @api.depends('product_label_ids')
    def _compute_single_label(self):
        if self.product_label_ids:
            self.single_label_id = self.product_label_ids[0]

    @api.depends('label_ids')
    def _get_user_printer_type(self):
        self.printer_type = self.env.user.context_def_label_printer.type

    @api.model
    def default_get(self, fields):
        ''' 
        To get default values for the object.
        '''
        product_label_obj = self.env['product.product.label']
        res = super(PrintPackBarcodeWizard, self).default_get(fields)
        product_ids = []
        
        product_product_ids = self.env.context.get('product_ids',False)
        
        if not product_product_ids:
            product_product_ids = self.env['product.product'].browse(self.env.context.get('active_ids'))
        
        if self.env.context.get('default_restrict_single',False) and len(product_product_ids) > 1:
            raise Warning(_('Printing multiple labels is restricted!'))
            
        for product_id in product_product_ids:
            if not product_id.default_code:
                raise UserError(msg=_("Product : %s not have default code" %(product_id.display_name)))
            
            codeparts = product_id.default_code.split('-')

            if len(codeparts) > 4:
                if codeparts[3]=='0':
                    if codeparts[2]=='0':
                        shortcode = ('-'.join(codeparts[0:2]))
                    else:
                        shortcode = ('-'.join(codeparts[0:3]))
                else:
                    shortcode = ('-'.join(codeparts[0:4]))
            else:
                shortcode = product_id.default_code

            nameline = 1
            nameL = {1:'',
                     2:'',
                     3:'',
                     4:''}

            for word in product_id.name.split():
                if len(nameL[nameline]+' '+word) < 27:
                    nameL[nameline]=(nameL[nameline]+' '+word).strip()
                else:
                    nameline = nameline +1
                    nameL[nameline] = (nameL[nameline] + ' ' + word).strip()


            product_label_id = product_label_obj.create({
                    'name': product_id.name,
                    'nameL1': nameL[1],
                    'nameL2': nameL[2],
                    'nameL3': nameL[3],
                    'nameL4': nameL[4],
                    'default_code': product_id.default_code,
                    'short_code': shortcode,
                    'note': '',
                    'label_to_print': 1,
                    'barcode': product_id.barcode,
                    'uom_name': product_id.uom_id.name,
                    'product_id': product_id.id,
            })
            product_ids.append(product_label_id.id)
        res.update({'product_label_ids': [(6, 0, product_ids)] or [],
                    'skip_first': False
                    })
        return res

    @api.multi
    def generate_labels(self):
        last_label = self.product_label_ids[0]
        leap_label = False
        Label_Res = []
        label_template_obj = self.env['label.twoinrow']
        for product_label in self.product_label_ids:
            product_label.pieces_in_pack = product_label.pieces_in_pack if product_label.product_id.uom_id.category_id.id != 1 else int(product_label.pieces_in_pack)
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
                    labels_to_print = labels_to_print -1

                if labels_to_print > 1:
                    # 1 1
                    Label_l = label_template_obj.create({
                        'first_label_empty': False,
                        'label1': product_label.id,
                        'second_label_empty': False,
                        'label2': product_label.id,
                        'copies_to_print': labels_to_print/2,
                    })
                    labels_to_print = labels_to_print - (int(labels_to_print/2)*2)
                    Label_Res.append(Label_l.id)
                if labels_to_print == 1:
                    leap_label = True
                    last_label = product_label
                    labels_to_print = 0
        if leap_label:
            Label_l = label_template_obj.create({
                #Tek last label
                'first_label_empty': False,
                'label1': product_label.id,
                'second_label_empty': True,
                'label2': product_label.id,
                'copies_to_print': 1,
                })
            Label_Res.append(Label_l.id)
        self.label_ids = [(6, 0, Label_Res)]
        return False


    @api.multi
    def show_label(self):
        self.generate_labels()
        datas = {
                'ids': self.env.context.get('active_ids'),
                'model': 'print.pack.barcode.wiz'
            }

        res = {
            'type' : 'ir.actions.report',
            'report_name': 'label_product_product',
            'datas' : datas,
        }



        return self.env.ref('product_label_print.label_product_product')\
            .with_context(active_model='print.pack.barcode.wiz').report_action(docids=self)



    @api.multi
    def print_label(self):
        self.generate_labels()
        printer = self.env.user.context_def_label_printer
        if not printer:
            raise Warning(_('You need to set a label printer in order to print.'))
        printer.print_document('product_label_print.label_product_product',
                               self.env.ref('product_label_print.label_product_product').render_qweb_text([self.id],
                               data={})[0],doc_form="txt")
        return {'type':'ir.actions.act_window_close'}

