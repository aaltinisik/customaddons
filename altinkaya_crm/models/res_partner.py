from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    vat_status = fields.Char(string="Vat Status", compute="_compute_vat_status")

    def _compute_vat_status(self):
        for partner in self:
            if partner.country_id.code == "TR" and partner.vat:
                vat_len = len(partner.vat)
                if vat_len == 10:
                    partner.vat_status = _("Company Tax No")

                elif vat_len == 11:
                    partner.vat_status = _("Individual Tax No")
                else:
                    partner.vat_status = _("Incorrect VAT")
            else:
                partner.vat_status = ""
        return True



