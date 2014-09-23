# -*- coding: utf-8 -*-
from openerp.osv import orm, fields

class hscode(orm.Model):
    _name = 'hscode'

    _columns = {
        'name': fields.char('Adı',required=True, size=100),
        'hscode': fields.char('GTIP', size=16),
        'nameen': fields.char('Name', size=100),
        'short_desc': fields.char('Short Description', size=50),
        'long_desc': fields.char('Long Description', size=200),
        'Kisa_aciklama': fields.char('Kısa Açıklama', size=50),
        'Uzun_aciklama': fields.char('Uzun Açıklama', size=200),
        'picture': fields.binary("Resim"),
        'notes': fields.text('Notlar'),
    }

    _order = "hscode"

