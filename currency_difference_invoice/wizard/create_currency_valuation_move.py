from odoo import models, api, fields, _
from odoo.exceptions import UserError


class CreateCurrencyValuationMove(models.TransientModel):
    _name = "create.currency.valuation.move"
    _description = "Transient Model For Currency Valuation Move"

    move_date = fields.Date(
        string="Move Date", required=True, default=fields.Date.context_today
    )

    @api.multi
    def create_move(self):
        context = dict(self._context or {})
        active_ids = context.get("active_ids", []) or []
        partners = self.env["res.partner"].browse(active_ids)
        created_move = partners.calc_currency_valuation(self.move_date)

        action = self.env.ref("account.action_move_journal_line")
        action_dict = action.read()[0]
        form_view = [(self.env.ref("account.view_move_form").id, "form")]
        if "views" in action_dict:
            action_dict["views"] = form_view + [(state, view) for state, view in action["views"] if view != "form"]
        else:
            action_dict["views"] = form_view
        action_dict["res_id"] = created_move.id

        return action_dict
