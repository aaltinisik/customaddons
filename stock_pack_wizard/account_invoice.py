# -*- coding: utf-8 -*-


from openerp.osv import osv, fields


class account_invoice(osv.osv):
    _inherit = "account.invoice"
    _columns = {
        'packing_tracking_ids': fields.one2many('stock.tracking', 'invoice_id', 'Packing Details'),
    }

    def btn_calc_weight_inv(self, cr, uid, ids, context=None):
        total_g, total_n, total_p = 0, 0, 0
        total_vol = total_air = total_land = 0

        tracking_ids = []
        for pack in self.browse(cr, uid, ids[0], context).packing_tracking_ids:
                total_g += pack.gross_weight
                total_n += pack.net_weight
                total_p += 1
                total_vol += (((pack.pack_h * pack.pack_w * pack.pack_l) * 1.0) / 1000000)
                total_air += math.ceil(((pack.pack_h * pack.pack_h * pack.pack_h) * 1.0) / 5000)
                total_land += math.ceil(((pack.pack_h * pack.pack_h * pack.pack_h) * 1.0) / 3000)
        vals = {
           'packing_tracking_ids': [(6, 0, tracking_ids)],
           'total_grosswg': total_g,
           'total_netwg': total_n,
           'total_num_pack': total_p,
           'total_volume': total_vol,
           'total_air': total_air,
           'total_land': total_land,
        }
        self.write(cr, uid, ids, vals, context)
        return True
    
        
account_invoice()