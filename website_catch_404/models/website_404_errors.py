# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, api, fields
from odoo.exceptions import ValidationError


class Website404Errors(models.Model):
    _name = "website.404.errors"
    _description = "Base Model for Website 404 Errors"

    name = fields.Char(string="URL")
    request_method = fields.Selection(
        selection=[
            ("GET", "GET"),
            ("POST", "POST"),
            ("PUT", "PUT"),
            ("DELETE", "DELETE"),
            ("HEAD", "HEAD"),
            ("OPTIONS", "OPTIONS"),
            ("PATCH", "PATCH"),
        ],
        string="Request Method",
    )
    hit_count = fields.Integer(string="Hit Count")
    website_id = fields.Many2one(
        comodel_name="website",
        string="Website",
        ondelete="cascade",
    )
    resolved = fields.Boolean(string="Resolved", default=False)

    @api.constrains("url")
    def _check_url(self):
        for record in self:
            if self.search_count([("name", "=", record.name)]) > 1:
                raise ValidationError("URL must be unique.")

    def action_create_redirect(self):
        self.ensure_one()
        aw_obj = self.env["ir.actions.act_window"]
        action = aw_obj._for_xml_id(
            "website_catch_404.wizard_create_redirect_from_404_action"
        )
        return action
