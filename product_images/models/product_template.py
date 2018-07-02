# -*- coding: utf-8 -*-
# © 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ProductTemplate(models.Model):
    
    _inherit = 'product.template'
     
    image_ids = fields.One2many('ir.attachment','product_tmpl_id',
                                 string='Other Images'
                                 )
