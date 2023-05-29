# Copyright 2023 Samet Altuntaş (https://github.com/samettal)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner.nace"

    full_partner_ids = fields.Many2many(
        string="NACE Partners",
        comodel_name="res.partner",
        compute="_compute_full_partner_ids",
        store=False,
    )

    full_partner_count = fields.Integer(
        string="Full partner count", compute="_compute_full_partner_ids", store=False
    )

    @api.multi
    def action_view_nace_partners(self):
        self.ensure_one()
        action = self.env.ref("base.action_partner_form").read()[0]
        action["domain"] = [("id", "in", self.full_partner_ids.ids)]
        return action

    @api.multi
    def _compute_full_partner_ids(self):
        for record in self:
            partner_ids = self.env["res.partner"].search(
                [
                    "|",
                    ("nace_id", "=", record.id),
                    ("secondary_nace_ids", "in", record.id),
                ]
            )
            record.full_partner_ids = [(6, 0, partner_ids.ids)]
            record.full_partner_count = len(partner_ids)
