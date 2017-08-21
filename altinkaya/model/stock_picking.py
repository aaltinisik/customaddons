# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class stock_picking(osv.osv):
    _inherit = "stock.picking"
    _columns = {
                'x_durum': fields.selection(
                                    [('1',u'İthal Eksik'),
                                     ('2',u'Kesimde'),
                                     ('3',u'Üretimde'),
                                     ('4',u'Montajda'),
                                     ('5',u'Çıkacak'),
                                     ('6',u'ACİL'),
                                     ('7',u'Müsteriyi Bekliyor')],
                                     'Durumu', select=True),
                'x_hazirlayan': fields.selection(
                                    [("Asim",u"Asım"),
                                     ("Muhammet","Muhammet"),
                                     ("Harun","Harun"),
                                     ("Sefer","Sefer")],
                                     u'Siparişi Hazırlayan', select=True),
                }
stock_picking()