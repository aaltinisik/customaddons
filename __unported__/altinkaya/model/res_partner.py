from openerp.osv import osv, fields


class res_partner(osv.Model):
    _inherit = 'res.partner'
    _columns = {
    'x_vergidairesi': fields.char('Vergi Dairesi', size=64, required=False),
    'x_vergino': fields.char('Vergi No', size=64, required=False,select=1),
    }
res_partner()