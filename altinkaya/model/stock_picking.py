# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class stock_picking(osv.osv):
    _inherit = "stock.picking"
    _columns = {
                'x_durum': fields.selection(
                                    [('1',u'İthal Eksik'),
                                     ('2',u'CNC Kesimde'),
                                     ('3',u'Enjeksiyonda'),
                                     ('4',u'Montajda'),
                                     ('5',u'Çıkacak'),
                                     ('6',u'ACİL'),
                                     ('7',u'Müsteriyi Bekliyor'),
                                     ('8',u'Profil Kesimde'),
                                     ('9', u'Sac Üretiminde'),
                                     ('A', u'Boyada'),
                                     ('B', u'Piyasadan Teminde')
                                     ],
                                     'Durumu', select=True),
                'x_hazirlayan': fields.selection(
                                    [("Asim",u"Asım"),
                                     ("Muhammet",u"Muhammet"),
                                     ("Harun",u"Harun"),
                                     ("Bilal", u"Bilal"),
                                     ("Saffet",u"Saffet"),
                                     ("Esra", u"Esra"),
                                     ("Selma", u"Selma"),
                                     (u"Uğur", u"Uğur"),
                                     (u"Çağrı", u"Çağrı"),
                                     ("Hatice", u"Hatice"),
                                     ("Muhsin", u"Muhsin")
                                     ],

                                     u'Siparişi Hazırlayan', select=True),
                'comment_irsaliye': fields.text(u'İrsaliye Notu'),
                'teslim_alan': fields.char(u'Malı Teslim Alan Ad Soyad', size=32)
                }
    
    def _prepare_shipping_invoice_line(self, cr, uid, picking, invoice, context=None):
        res = super(stock_picking, self)._prepare_shipping_invoice_line(cr, uid, picking, invoice, context=context)
        if picking.carrier_id:
            invoice.carrier_id = picking.carrier_id
        if res and res.get('name',False) and ['name'].__contains__('Teslim'):
            invoice.address_contact_id = ''
        if res and res.get('price_unit',0.0) <= 0.0:
            return None
        return res

    
stock_picking()
