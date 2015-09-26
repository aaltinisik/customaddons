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
from openerp.osv import osv, fields
import math


class account_invoice(osv.osv):
    _inherit = "account.invoice"
    _columns = {
        'packing_tracking_ids': fields.one2many('stock.tracking', 'picking_out_id', 'Packing Details'),
        'total_grosswg': fields.float('Total Gross Weight'),
        'total_netwg': fields.float('Total Net Weight'),
        'total_volume': fields.float('Total Volume'),
        'total_land': fields.integer('Total Land Weight'),
        'total_air': fields.integer('Total Air Weight'),
        'waybillno': fields.char('Way Bill no.', size=64),
        'currency_at_date': fields.float('Currency Rate'),
        'carrier_id':fields.many2one('delivery.carrier', "Carrier"),
        'total_num_pack': fields.integer('Total Packages'),
    }

    def _get_currency_rate(self, cr, uid, ids, context=None):
        currency_rate = 0
        rate = self.browse(cr, uid, ids[0]).currency_id.rate
        if rate != 0:
            currency_rate = 1.00 / (rate + 0.0)
        return currency_rate

    def btn_calc_weight_inv(self, cr, uid, ids, context=None):
        total_g = total_n = total_c = 0
        total_vol = total_air = total_land = 0
        lines = self.browse(cr, uid, ids[0], context).packing_tracking_ids
        for pack in lines:
            total_g += pack.gross_weight
            total_n += pack.net_weight
            total_c += 1
            total_vol += (((pack.pack_h * pack.pack_w * pack.pack_l) * 1.0) / 1000000)
            total_air += math.ceil(((pack.pack_h * pack.pack_h * pack.pack_h) * 1.0) / 5000)
            total_land += math.ceil(((pack.pack_h * pack.pack_h * pack.pack_h) * 1.0) / 3000)
        vals = {
           'total_grosswg': total_g,
           'total_netwg': total_n,
           'total_volume': total_vol,
           'total_air': total_air,
           'total_land': total_land,
           'currency_at_date': self._get_currency_rate(cr, uid, ids),
           'total_num_pack': total_c
        }
        self.write(cr, uid, ids, vals, context)
        return True

    def action_date_assign(self, cr, uid, ids, *args):
        res = super(account_invoice, self).action_date_assign(cr, uid, ids, *args)
        self.btn_calc_weight_inv(cr, uid, ids)
        return res

account_invoice()
