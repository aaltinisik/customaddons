# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models


class Website(models.Model):
    _inherit = "website"

    def get_pricelist_available(self, show_visible=False):
        """
        Override to show partner pricelist if it is not selectable.
        Maybe we don't need this method since we have get_current_pricelist inherited.
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
            return partner_pricelist

        return self.env["product.pricelist"].browse(pricelist_ids)

    def get_current_pricelist(self):
        """
        Returns the current pricelist for the current user.
        If the user is logged in and has a pricelist set on the partner, it will be chosen.
        """
        res = super(Website, self).get_current_pricelist()
        website = self.with_company(self.company_id)
        partner = website.env.user.partner_id
        if partner and partner.website_pricelist_id:
            return partner.website_pricelist_id
        return res
