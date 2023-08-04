# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, api, fields
from datetime import datetime, timedelta


class Website(models.Model):
    _inherit = "website"

    brand_name = fields.Char(
        string="Brand Name",
        help="The name of the brand of the website,"
        " this will shown in the Product Schema",
    )
    delivery_min_time = fields.Integer(
        string="Delivery Minimum Time",
        help="The minimum time for delivery in days,"
        " this will shown in the Product Schema",
    )
    delivery_max_time = fields.Integer(
        string="Delivery Maximum Time",
        help="The maximum time for delivery in days,"
        " this will shown in the Product Schema",
    )

    price_validity_date = fields.Datetime(
        string="Price Validity Date",
        compute="_compute_price_validity_date",
    )

    def _compute_price_validity_date(self):
        for record in self:
            record.price_validity_date = datetime.now() + timedelta(days=60)
