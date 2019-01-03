# -*- encoding: utf-8 -*-


from openerp.osv import osv

class stockmove(osv.osv):
    _inherit = "stock.move"

    def _get_invoice_line_vals(self, cr, uid, move, partner, inv_type, context=None):
        res = super(stockmove, self)._get_invoice_line_vals(cr, uid, move, partner, inv_type, context=context)
        res.update({
            'hscode_id': move.product_id.hscode_id.id or move.product_id.categ_id.hscode_id.id,
        })
        return res
