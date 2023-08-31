# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class WizardCreateRedirectFrom404(models.TransientModel):
    _name = "wizard.create.redirection.from.404"
    _description = "Wizard Create Redirect From 404"

    record_404_id = fields.Many2one(
        "website.404.errors",
        string="404 Error",
        required=True,
        readonly=True,
        ondelete="cascade",
    )

    url_from = fields.Char(
        string="URL From",
        compute="_compute_url_from",
    )

    url_to = fields.Char(
        string="URL To",
        required=True,
    )

    def _compute_url_from(self):
        for record in self:
            record.url_from = record.record_404_id.name

    def default_get(self, fields):
        res = super(WizardCreateRedirectFrom404, self).default_get(fields)
        res["record_404_id"] = self.env.context.get("active_id")
        return res

    def action_create_redirect(self):
        self.ensure_one()

        if not self.url_to.startswith("/"):
            raise UserError(_("URL To must start with a slash (/)."))

        if self.record_404_id.resolved:
            raise UserError(_("This 404 error is already resolved."))

        self.env["website.rewrite"].create(
            {
                "url_from": self.record_404_id.name,
                "url_to": self.url_to,
                "redirect_type": "301",
                "name": _("Website 404 Error Resolved"),
                "website_id": self.record_404_id.website_id.id,
            }
        )
        self.record_404_id.resolved = True
        return True
