# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    allow_filling = fields.Boolean(
        string="Allow Filling",
        help="If checked, attribute values will be filled automatically",
        default=True,
    )

    visibility = fields.Selection(
        selection=[
            ('visible', 'Visible on eCommerce'),
            ('hidden', 'Hidden'),
        ],
        string='Visibility',
        default='visible',
    )
