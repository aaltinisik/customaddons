from openerp import api, fields, models, _


class res_partner_worksector(models.Model):
    _name = 'res.partner.worksector'

    description = fields.Text(string="Description", translate=True)
    name = fields.Char(string="Name", translate=True)
    partner_ids = fields.One2many('worksector.line', 'worksector_id', string="Partner")
    product_categ_ids = fields.One2many('product.category.line', 'worksector_id', string="Category")


class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    @api.depends('worksector_ids')
    def _get_product_categ(self):
        for part in self:
            lst = []
            for line in part.worksector_ids:
                lst += [x.product_categ_id.id for x in line.worksector_id.product_categ_ids]
            part.target_product_categ_ids = self.env['product.category'].browse(set(lst))

    worksector_ids = fields.One2many('worksector.line', 'partner_id', string="Worksector")
    target_product_categ_ids = fields.Many2many('product.category', compute="_get_product_categ", store=True)


class worksector_line(models.Model):
    _name = 'worksector.line'

    partner_id = fields.Many2one('res.partner', string="Partner")
    worksector_id = fields.Many2one('res.partner.worksector', string="worksector")


class product_category_line(models.Model):
    _name = 'product.category.line'

    product_categ_id = fields.Many2one('product.category', string="Product Category")
    worksector_id = fields.Many2one('res.partner.worksector', string="worksector")
