# -*- coding: utf-8 -*-


from openerp.osv import osv, fields


class account_invoice(osv.osv):
    _inherit = "account.invoice"
    _columns = {
        'packing_tracking_ids': fields.one2many('stock.tracking', 'invoice_id', 'Packing Details'),
    }
    
account_invoice()