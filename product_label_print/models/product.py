# -*- coding: utf-8 -*-

from openerp import api, fields, models, _


class product_product(models.Model):
    _inherit = "product.product"

    label_to_print = fields.Integer(string='# of label to be printed', default=1)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
