from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _search_my_team(self, operator, operand):
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

    my_team = fields.Boolean(
        "My Team",
        compute="_compute_my_team",
        search="_search_my_team",
        store=False,
    )

    @api.multi
    def _compute_my_team(self):
        for rec in self:
            if self.env.user in rec.team_id.member_ids:
                rec.my_team = True
            else:
                rec.my_team = False


