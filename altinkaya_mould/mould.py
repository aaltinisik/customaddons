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
from openerp.osv import orm, fields


class mould(orm.Model):
    _name = 'mould'

    _columns = {
        'code': fields.char('Kodu', size=32),
        'name': fields.char('Adı',required=True, size=100),
        'parent_id':fields.many2one('mould', 'Ana Kalıp Referansı', ondelete='cascade', select=True),
        'is_parent': fields.boolean('Ana Kalıp Mı?'),
        'type': fields.selection([
            ('enjeksiyon', 'Enjeksiyon'),
            ('kesme_kalıbı', 'Kesme Kalıbı'),
            ('bükme_kalıbı', 'Bükme Kalıbı'),
            ('diğer_kalıplar', 'diğer Kalıplar'),
            ], 'Kalıbın Cinsi'),
        'numcores': fields.integer('Göz Sayısı'),
        'dailycapacity': fields.integer('Günlük Üretim Kapasitesi'),
        'material_id': fields.many2one('product.product', 'Kullanılan Malzeme'),
        'product_ids': fields.many2many('product.product', 'mould_product_rel', 'mould_id', 'product_id' , 'Üretilen Ürünler'),
        'partner_id': fields.many2one('res.partner', 'Varsa ilgili Müşteri'),
        'owner': fields.many2one('res.partner', 'Kalıbın Sahibi'),
        'picture': fields.binary("Resim"),
        'notes': fields.text('Notlar'),
        'mould_ids': fields.one2many('mould','parent_id','Kalıbın Maçaları'),
        'sequence': fields.integer('Sıra'),
    }

    _order = "parent_id,sequence,code"

    _defaults = {
        'numcores' : 1,
        'dailycapacity': 1
    }


