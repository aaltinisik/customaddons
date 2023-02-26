# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sale_price = fields.Float(
        string="Sale Price", help="Dummy price field for product.template", default=0.0
    )
