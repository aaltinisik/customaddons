# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2013-Present Acespritech Solutions Pvt. Ltd. (<http://acespritech.com>).
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


class ProductMould(models.Model):
    _name = 'product.mould'
    _order = "parent_id,sequence,code"
    
    code =  fields.Char('Code', size=32)
    name = fields.Char('Name',required=True, size=100)
    parent_id = fields.Many2one('product.mould', 'Main Mould Ref', ondelete='cascade')
    is_parent= fields.Boolean('Main Mould?')
    type = fields.Selection([('injection', 'Injection'),
            ('cut', 'Cut-off Mould'),
            ('bend', 'Bend Mould'),
            ('other', 'Other Moulds'),
            ], 'Mould Type')
    numcores = fields.Integer('#Eye',default=1)
    dailycapacity = fields.Integer('Daily Production Capacity',default=1)
    material_id =  fields.Many2one('product.product', 'Use Material')
    product_ids =  fields.Many2many('product.product', 'mould_product_rel', 'mould_id', 'product_id' , 'Produced Products')
    partner_id =  fields.Many2one('res.partner', 'Partner')
    owner_id =fields.Many2one('res.partner', 'Owner')
    image = fields.Binary("Image")
    notes =  fields.Text('Notes')
    mould_ids = fields.One2many('product.mould','parent_id','Core Mould')
    sequence = fields.Integer('Sequence')




