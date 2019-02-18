# -*- coding: utf-8 -*-
# © 2009-2016 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    currency_rate_type_id = fields.Many2one('res.currency.rate.type',
                                            string='Default Currency Rate Type')

    # Activate the currency update
    auto_currency_up = fields.Boolean(
        string='Automatic Currency Rates Download', default=True,
        help="Automatic download of currency rates for this company")

    # List of services to fetch rates
    services_to_use = fields.One2many(
        'currency.rate.update.service',
        'company_id',
        string='Currency update services')

    @api.multi
    def button_refresh_currency(self):
        """Refresh the currencies rates !!for all companies now"""
        self.services_to_use.refresh_currency()
