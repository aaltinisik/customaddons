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

from openerp import models, fields, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class producttemplate(models.Model):
    _inherit = "product.template"

    @api.one
    def _calculate_weight_air(self):
        packed_volume = 0.0
        pack_weight = 0.0  # in gr
        air_weight = 0.0  # in gr
        item_weight = 0.0  # in gr
        volume = self.width * self.height * self.length
        weight_net = 0.0
        air_weight = 0.0
        if self.weight_measured == 0:
            item_weight = weight_net * 1000  # weight_net in gr
        else:
            item_weight = self.weight_measured
        if self.pack_product and self.pack_product.weight != 0 and self.pack_product.length != 0 and self.pack_product.width != 0 and self.pack_product.weight_measured != 0:
            packed_volume = self.pack_product.length * self.pack_product.width * self.pack_product.height / self.pieces_in_pack
            air_weight = (self.pack_product.weight_measured + (self.pieces_in_pack * item_weight)) / self.pieces_in_pack
        else:
            air_weight = item_weight * 1.15
            packed_volume = volume * 1.15

        if (packed_volume / 5.0) > air_weight:  # if volume is important
            self.weight_air = packed_volume / 5.0
        else:
            self.weight_air = air_weight

    @api.one
    def _calculate_weight_ground(self):
        packed_volume = 0.0
        pack_weight = 0.0  # in gr
        ground_weight = 0.0  # in gr
        item_weight = 0.0  # in gr
        volume = self.width * self.height * self.length
        weight_net = 0.0
        ground_weight = 0.0
        if self.weight_measured == 0:
            item_weight = weight_net * 1000  # weight_net in gr
        else:
            item_weight = self.weight_measured
        if self.pack_product and self.pack_product.weight != 0 and self.pack_product.length != 0 and self.pack_product.width != 0 and self.pack_product.weight_measured != 0:
            packed_volume = self.pack_product.length * self.pack_product.width * self.pack_product.height / self.pieces_in_pack
            ground_weight = (self.pack_product.weight_measured + (self.pieces_in_pack * item_weight)) / self.pieces_in_pack
        else:
            ground_weight = item_weight * 1.15
            packed_volume = volume * 1.15

        if (packed_volume / 3.0) > ground_weight:  # if volume is important
            self.weight_ground = packed_volume / 3.0
        else:
            self.weight_ground = ground_weight



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
    weight_ground = fields.Float(
        string=_("Weight for Ground Transport (gr)"),
        compute='_calculate_weight_ground'
    )
    weight_air = fields.Float(
        string=_("Weight for Air Transport (gr)"),
        compute='_calculate_weight_air'
    )
