# -*- coding: utf-8 -*-
# © 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3).

from openerp import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"
    
    image_ids = fields.One2many('ir.attachment',
        compute="_compute_image_ids" , inverse='_inverse_image_ids',
        string="Images")
    
   

    @api.one
    @api.depends('product_tmpl_id', 'product_tmpl_id.image_ids')
    def _compute_image_ids(self):
        self.image_ids = self.product_tmpl_id.image_ids.filtered(lambda i:i.product_id.id in [False, self.id])
        

    @api.one
    def _inverse_image_ids(self):
        deleted = self.product_tmpl_id.image_ids - self.image_ids
        self.product_tmpl_id.image_ids = self.product_tmpl_id.image_ids  - deleted | self.image_ids
    

    @api.multi
    def unlink(self):
        for product in self:
            product.image_variant_ids.unlink()

        return super(ProductProduct, self).unlink()


