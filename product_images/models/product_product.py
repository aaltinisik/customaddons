# -*- coding: utf-8 -*-
# © 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3).

from openerp import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"
    
    image_ids = fields.One2many('ir.attachment',
        compute="_compute_image_ids" ,
        string="Images")
    
    image_variant_ids = fields.One2many('ir.attachment','product_id',
                                 string='Variant Images'
                                 )

    @api.one
    @api.depends('product_tmpl_id', 'product_tmpl_id.image_ids')
    def _compute_image_ids(self):
        self.image_ids = self.product_tmpl_id.image_ids | self.image_variant_ids
        


    @api.multi
    def unlink(self):
        for product in self:
            product.image_variant_ids.unlink()

        return super(ProductProduct, self).unlink()


