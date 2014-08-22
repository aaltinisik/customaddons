from openerp.osv import osv, fields


class stock_picking_out(osv.osv):
    _inherit = "stock.picking.out"
    _columns = {
        'x_durum': fields.selection(
                                    [('0','Not urgent'),
                                     ('1','Normal'),
                                     ('2','Urgent'),
                                     ('3','Very Urgent')],
                                     'Durum', select=True),
      'x_hazirlayan': fields.selection(
                                    [('0','Not urgent'),
                                     ('1','Normal'),
                                     ('2','Urgent'),
                                     ('3','Very Urgent')],
                                     'Siparisi Hazirlayan', select=True),

                }
stock_picking_out()