# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    website_pricelist_id = fields.Many2one(
        "product.pricelist", string="Website Pricelist"
    )

    ecommerce_partner = fields.Boolean(
        string="E-commerce Partner",
        help="If checked, this partner is an e-commerce partner.",
    )

    # @api.multi
    # def name_get(self):
    #     result = []
    #     for partner in self:
    #         if partner.ecommerce_partner:
    #             result.append((partner.id, _("[E-Commerce]") + " " + partner.name))
    #         else:
    #             result.append((partner.id, partner.name))
    #     return result