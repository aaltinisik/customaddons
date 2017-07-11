# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    This module copyright (C) 2017 Ahmet Altinisik#    (http://www.altinkaya.com.tr).#
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

from openerp import models, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class product_template(models.Model):
    _inherit = "product.template"

    pack_product = fields.Many2one(
        "product.product",
        string=_("Product of Package"),
        required=False,
        translate=False,
        readonly=False,
    )
    width = fields.Float(
        string=_("Measured Width (cm)"),
        required=False,
        translate=False,
        readonly=False,
    )
    length = fields.Float(
        string=_("Measured Length (cm)"),
        required=False,
        translate=False,
        readonly=False,
    )
    pieces_in_pack = fields.Float(
        string=_("Pieces in related pack"),
        required=False,
        translate=False,
        readonly=False,
    )
    height = fields.Float(
        string=_("Measured Height (cm)"),
        required=False,
        translate=False,
        readonly=False,
    )
    weight_measured = fields.Float(
        string=_("Measured weight (gr)"),
        required=False,
        translate=False,
        readonly=False,
        digits_compute=dp.get_precision('Stock Weight')
    )