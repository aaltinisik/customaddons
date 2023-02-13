# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"
    _order = "ranking, name"
    tax_office_name = fields.Char(
        string="Tax Office Name",
        help="Tax Office Name",
        copy=False,
    )

    ranking = fields.Integer(
        string="Ranking",
        default=999999,
        readonly=True,
    )

    @api.constrains("vat", "country_id")
    def check_vat(self):
        """This method"""
        for partner in self:
            if partner.vat == "11111111111" or partner.vat == "2222222222":
                return False
            if not partner.vat or partner.vat == "False":
                return False
            if partner.parent_id:
                return False
            colliding_partner = self.search(
                [
                    ("vat", "=", partner.vat),
                    ("id", "!=", partner.id),
                    ("is_company", "=", 1),
                ],
                limit=1,
            )
            colliding_partner = self.browse(colliding_partner.id)
            if (
                colliding_partner
                and colliding_partner.company_id.id == partner.company_id.id
            ):
                if (
                    colliding_partner.commercial_partner_id
                    != partner.commercial_partner_id
                ):
                    raise UserError(
                        _(
                            "The VAT number [%s] for this partner is also registered"
                            " with partner [%s] Each partner should have unique vat number."
                        )
                        % (colliding_partner[0].vat, colliding_partner[0].name)
                    )
            else:
                # TDE Fix false return should raise
                self.check_vat_tr(partner.vat)
        return super(ResPartner, self).check_vat()
