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


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_currency_rate_type_id = fields.Many2one('res.currency.rate.type', company_dependent=True,
        string ='Customer Currency Rate Type',
        help="This currency rate type will be used instead of the default one for sale orders and customer invoices")

    supplier_currency_rate_type_id = fields.Many2one('res.currency.rate.type', company_dependent=True,
        string ='Supplier Currency Rate Type',
        help="This currency rate type will be used instead of the default one for purchase orders and supplier invoices")
