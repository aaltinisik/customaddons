# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    website_pricelist_id = fields.Many2one(
        comodel_name="product.pricelist",
        string="Website Pricelist",
        help="Pricelist for website",
    )
