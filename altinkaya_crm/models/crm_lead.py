from odoo import models, fields, api


class CRMLead(models.Model):
    _inherit = "crm.lead"

    linkedin = fields.Char(string="LinkedIn")

    @api.model
    def _search_my_team_activity(self, operator, operand):
        if operator == "=":
            new_operator = "in"
        else:
            new_operator = "not in"
        res = self.search(
            [
                ("team_id.member_ids", new_operator, self.env.user.id),
            ],
        )
        return [("id", "in", res.ids)]

    my_team_activity = fields.Boolean(
        "My Team Activity",
        compute="_compute_my_team_activity",
        search="_search_my_team_activity",
        store=False,
    )

    @api.multi
    def _compute_my_team_activity(self):
        for lead in self:
            if self.env.user in lead.team_id.member_ids:
                lead.my_team_activity = True
            else:
                lead.my_team_activity = False



