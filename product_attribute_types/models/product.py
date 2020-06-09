# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from odoo import api, fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    attr_type = fields.Selection(required=True, selection=[
        ('select', 'Select'),
        ('range', 'Range'),
        ('numeric', 'Numeric')], string="Type", default='select')


class ProductAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    required = fields.Boolean('Required')
    default = fields.Many2one('product.attribute.value', 'Default')
    attr_type = fields.Selection(string='Type', store=False,
                                 related='attribute_id.attr_type')


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    attr_type = fields.Selection(string='Type',
                                 related='attribute_id.attr_type')
    numeric_value = fields.Float('Numeric Value', digits=(12, 6))
    min_range = fields.Float('Min', digits=(12, 6))
    max_range = fields.Float('Max', digits=(12, 6))

    @api.onchange('name')
    def onchange_name(self):
        if self.attr_type == 'numeric':
            try:
                self.numeric_value = float((''.join([c for c in self.name if c in '1234567890,.'])).replace(',', '.'))
                self.attribute_code = (''.join([c for c in self.name if c in '1234567890,.'])).replace(',', '').replace('.', '')
            except Exception:
                pass

    @api.one
    def write(self, vals):
        if vals.get('name',False):
            if vals.get('attr_type') == 'numeric' or self.attr_type == 'numeric':
                if vals.get('numeric_value',0.0) == 0.0 or self.numeric_value == 0.00:
                    try:
                        vals['numeric_value'] = float((''.join([c for c in vals.get('name','') if c in '1234567890,.'])).replace(',', '.'))
                    except Exception:
                        pass
        return super(ProductAttributeValue, self).write(vals)

    @api.model
    def create(self, vals):
        create_vals = super(ProductAttributeValue, self).create(vals)
        if vals.get('name',False):
            if create_vals['attr_type'] == 'numeric':
                if create_vals['numeric_value'] == 0.0:
                    try:
                        create_vals['numeric_value'] = float((''.join([c for c in vals.get('name','') if c in '1234567890,.'])).replace(',', '.'))
                    except Exception:
                        pass

                if create_vals['numeric_value'] != 0.0:
                    try:
                        create_vals['attribute_code'] = (''.join([c for c in vals.get('name','') if c in '1234567890,.'])).\
                            replace(',','').replace('.', '')
                    except Exception:
                        pass

        return create_vals
