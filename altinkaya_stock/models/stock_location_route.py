# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api
from odoo.tools.translate import html_translate


class StockLocationRouteInherit(models.Model):
    """
    Inherit stock.location.route model to add mail activity
    """

    _name = "stock.location.route"
    _inherit = ["mail.thread", "stock.location.route"]

    description = fields.Html(
        "Description for routes",
        sanitize_attributes=False,
        translate=html_translate,
        copy=False,
        track_visibility="onchange",
    )

    #  Add tracking to the field
    sequence = fields.Integer(track_visibility="onchange")
    active = fields.Boolean(track_visibility="onchange")
    name = fields.Char(track_visibility="onchange")

    @api.multi
    def write(self, vals):
        """Track rule_ids field changes."""
        msg = {}
        for route in self:
            if "rule_ids" in vals:
                msg.update(
                    {
                        route: '<span style="font-weight:bold;">Rota kuralları değişti.<br></span>'
                        '<span style="font-weight:bold;">Eski kurallar:</span><br>'
                        "%s" % "<br>".join(route.rule_ids.mapped("name"))
                    }
                )
        res = super(StockLocationRouteInherit, self).write(vals)
        for route in self:
            if "rule_ids" in vals:
                msg[route] += (
                    '<br><span style="font-weight:bold;">Yeni kurallar:</span><br>%s'
                    % "<br>".join(route.rule_ids.mapped("name"))
                )
                route.message_post(body=msg[route])
        return res
