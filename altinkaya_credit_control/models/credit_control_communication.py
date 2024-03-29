# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from base64 import b64encode


class CreditControlCommunication(models.Model):
    _inherit = "credit.control.communication"

    communication_channel = fields.Selection(
        related="policy_level_id.channel", readonly=True
    )

    credit_control_lines_html = fields.Html(
        "Credit Control Lines",
        compute="_compute_credit_control_lines_html",
        store=False,
    )

    state = fields.Selection(
        [("draft", "Draft"), ("sent", "Sent"), ("done", "Done")],
        string="Status",
        readonly=True,
        copy=False,
        index=True,
        default="draft",
        track_visibility="onchange",
    )

    @api.one
    def action_send_email(self):
        """
        Send account follow-up email to the customer.
        :return:
        """
        self.ensure_one()
        if self.communication_channel != "email":
            return False  # Maybe we should raise an error here.

        if self.state in ("sent", "done"):
            raise ValidationError(_("This communication is already sent."))

        lines_2be_processed = self.credit_control_line_ids.filtered(
            lambda line: line.state != "sent"
        )

        if not lines_2be_processed:
            raise ValidationError(_("There is no draft lines to send."))

        self = self.with_context(lang=self.partner_id.lang)

        partner = self.partner_id
        mail_template = self.policy_level_id.email_template_id
        # Send the email
        partner.with_context(credit_control_mail=True).message_post_with_template(
            template_id=mail_template.id,
            model=self._name,
            res_id=self.id,
        )
        # Set the state of the credit control lines to "queued"
        lines_2be_processed.write({"state": "sent"})
        self.state = "sent"

    def _compute_credit_control_lines_html(self):
        """
        This method renders the qweb template and returns the result as HTML.
        :return: HTML string
        """
        for comm in self:
            comm.credit_control_lines_html = (
                self.env["ir.qweb"]
                .render(
                    "altinkaya_credit_control.report_credit_control_lines",
                    values={"doc": self},
                )
                .decode("utf8")
            )
        return True

    def _get_partner_statement_report(self):
        """
        Render the partner statement report and return the result as PDF.
        :return:
        """
        if self._context.get("lang") == "tr_TR":
            report_name = "altinkaya_reports.partner_statement_altinkaya"
        else:
            report_name = "altinkaya_reports.partner_statement_altinkaya_en"
        statement_report = self.env.ref(report_name)
        return statement_report.render_qweb_pdf(self.partner_id.id)[0]

    def action_set_done(self):
        """
        Set the state of the communication to "done"
        :return: bool
        """
        self.ensure_one()
        self.write({"state": "done"})
        self.credit_control_line_ids.write({"state": "done"})
        return True
