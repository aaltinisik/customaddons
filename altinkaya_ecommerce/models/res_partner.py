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

    @api.multi
    def name_get(self):
        """
        Inherit to add [E] prefix to e-commerce partners.
        :return:
        """
        res = super(ResPartner, self).name_get()
        result = []
        ecommerce_partners = self.filtered(lambda p: p.ecommerce_partner).ids
        for partner in res:
            if partner[0] in ecommerce_partners:
                partner = (partner[0], "[E] " + partner[1])
            else:
                partner = (partner[0], partner[1])
            result.append(partner)
        return result
