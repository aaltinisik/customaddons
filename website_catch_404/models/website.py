# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields
from urllib.parse import urlparse, urlunparse


def remove_domain_and_protocol(url):
    """
    Removes domain and protocol from the url.
    """
    parsed_url = urlparse(url)
    modified_url = urlunparse(
        (
            "",
            "",
            parsed_url.path,
            parsed_url.params,
            parsed_url.query,
            parsed_url.fragment,
        )
    )
    return modified_url


class Website(models.Model):
    _inherit = "website"

    catch_404_errors = fields.Boolean(string="Catch 404 Errors")
    catched_404_errors = fields.One2many(
        comodel_name="website.404.errors",
        inverse_name="website_id",
        string="Catched 404 Errors",
    )

    def _catch_404_error(self, request):
        url = remove_domain_and_protocol(request.url)
        request_method = request.method
        website_id = self.id
        error = (
            self.env["website.404.errors"]
            .sudo()
            .search([("name", "=", url), ("website_id", "=", website_id)])
        )
        if error:
            error.hit_count += 1
        else:
            self.env["website.404.errors"].sudo().create(
                {
                    "name": url,
                    "request_method": request_method,
                    "hit_count": 1,
                    "website_id": website_id,
                }
            )
        self.env.cr.commit()
        return True
