# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015, Eska Yazılım ve Danışmanlık A.Ş.
#    http://www.eskayazilim.com.tr
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from odoo import models, fields


class CurrencyRateUpdateType(models.Model):
    _name = 'currency.rate.update.type'
    _description = 'Currency Rate Update Types'

    service_id = fields.Many2one('currency.rate.update.service', string='Service', required=True)

    service_rate_type = fields.Selection(
        [
            ('forex_buy', 'Forex Buy'),
            ('forex_sell', 'Forex Sell'),
            ('banknote_buy', 'Banknote Buy'),
            ('banknote_sell', 'Banknote Sell'),
        ],
        string='Service Rate Type')

    currency_rate_type_id = fields.Many2one('res.currency.rate.type', string='System Rate Type')

