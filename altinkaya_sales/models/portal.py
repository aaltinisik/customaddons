import uuid
import hashlib
import hmac
from werkzeug.urls import url_encode
from odoo import api, exceptions, fields, models, tools, _


class PortalMixinInheritance(models.AbstractModel):
    _inherit = "portal.mixin"

    @api.multi
    def get_portal_url(
        self,
        suffix=None,
        report_type=None,
        download=None,
        query_string=None,
        anchor=None,
    ):
        """
        Changes the invoice download link in the portal to e-invoice.
        """
        self.ensure_one()
        if self._name == "account.invoice" and self.einvoice_pdf_id:
            invoice_url = f"/report/einvoicepdf/{self.id}" + "?access_token=%s" % (
                self._portal_ensure_token(),
            )
            return invoice_url

        else:
            return super(PortalMixinInheritance, self).get_portal_url(
                suffix=suffix,
                report_type=report_type,
                download=download,
                query_string=query_string,
                anchor=anchor,
            )
