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
                                     ("Muharrem", "Muharrem"),
                                     ("Sefer","Sefer")],
                                     u'Siparişi Hazırlayan', select=True),
                }
    
    def _prepare_shipping_invoice_line(self, cr, uid, picking, invoice, context=None):
        res = super(stock_picking, self)._prepare_shipping_invoice_line(cr, uid, picking, invoice, context=context)
        if picking.carrier_id:
            invoice.carrier_id = picking.carrier_id
        if res['name'].__contains__('Teslim'):
            invoice.address_contact_id = ''
        if res and res.get('price_unit',0.0) <= 0.0:
            return None
        return res

    
stock_picking()
