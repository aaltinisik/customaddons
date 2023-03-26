# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models


class Website(models.Model):
    _inherit = "website"

    def get_pricelist_available(self, show_visible=False):
        """Return the list of pricelists that can be used on website for the current user.
        Country restrictions will be detected with GeoIP (if installed).
        :param bool show_visible: if True, we don't display pricelist where selectable is False (Eg: Code promo)
        :returns: pricelist recordset
        """
        self.ensure_one()
        website = self.with_company(self.company_id)
        partner_sudo = website.env.user.partner_id
        is_user_public = self.env.user._is_public()
        if not is_user_public:
            partner_pricelist = partner_sudo.website_pricelist_id
        else:  # public user: do not compute partner pl (not used)
            partner_pricelist = self.env["product.pricelist"]
        website_pricelists = website.sudo().pricelist_ids
        pricelist_ids = website_pricelists.filtered(lambda pl: pl.selectable).ids
        if partner_pricelist:
            pricelist_ids.append(partner_pricelist.id)

        return self.env["product.pricelist"].browse(pricelist_ids)
