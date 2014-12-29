# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class stock_picking_out(osv.osv):
    _inherit = "stock.picking.out"
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
                                    [(u'Asım',u'Asım'),
                                     ("Can","Can"),
                                     ("Harun","Harun"),
                                     ("Sefer","Sefer")],
                                     u'Siparişi Hazırlayan', select=True),
                }
stock_picking_out()