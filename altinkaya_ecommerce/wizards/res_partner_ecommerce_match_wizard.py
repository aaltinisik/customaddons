# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartnerEcommerceMatchWizard(models.TransientModel):
    _name = "res.partner.ecommerce.match.wizard"
    _description = "E-commerce Partner Match Wizard"

    match_lines = fields.One2many(
        "res.partner.ecommerce.match.wizard.line",
        "match_id",
        string="Match Lines",
    )

    # @api.model
    # def default_get(self, fields_list):
    #     res = super(ResPartnerEcommerceMatchWizard, self).default_get(fields_list)
    #     ecommerce_partners = self.env["res.partner"].search(
    #         [("ecommerce_partner", "=", True), ("parent_id", "=", False)]
    #     )
    #     match_lines = []
    #     for partner in ecommerce_partners:
    #         match_lines.append(
    #             (0, 0, {"ecommerce_partner_id": partner.id, "partner_id": False})
    #         )
    #     res["match_lines"] = match_lines
    #     return res

    @api.model
    def create(self, vals):
        """
        Inherit to add carrier prices to the wizard.
        :param vals: dict
        :return: recordset
        """
        res = super(ResPartnerEcommerceMatchWizard, self).create(vals)
        for wizard in res:
            ecommerce_partners = self.env["res.partner"].search(
                [("ecommerce_partner", "=", True), ("parent_id", "=", False)]
            )
            match_lines = []
            for partner in ecommerce_partners:
                match_lines.append(
                    (0, 0, {"ecommerce_partner_id": partner.id, "partner_id": False})
                )
            wizard.match_lines = match_lines
        return res
    def action_get_wizard(self):
        """Create wizard to match partners."""
        view = self.env.ref("altinkaya_ecommerce.view_res_partner_ecommerce_match_wizard_form")

        match_wizard = self.create({})
        return {
            "name": _("Match E-commerce Partners"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_id": match_wizard.id,
            "res_model": "res.partner.ecommerce.match.wizard",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
        }

    def action_match(self):
        for line in self.match_lines.filtered(lambda l: l.partner_id):
            line.ecommerce_partner_id.parent_id = line.partner_id
        self.env.cr.commit()
        return True


class ResPartnerEcommerceMatchWizardLine(models.TransientModel):
    _name = "res.partner.ecommerce.match.wizard.line"
    _description = "E-commerce Partner Match Wizard Line"

    ecommerce_partner_id = fields.Many2one(
        "res.partner",
        string="E-commerce Partner",
        required=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
    )
    match_id = fields.Many2one(
        "res.partner.ecommerce.match",
        string="Match",
        required=True,
    )
