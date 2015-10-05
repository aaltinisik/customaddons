from openerp.osv import osv, fields


class x_makine(osv.Model):
    _name = 'x_makine'  
    _columns = {
        'x_group': fields.char(
            'Bolum',
            size=128,
            required=False),
        'x_kod': fields.char(
            'Makine Kodu',
            size=128,
            required=False),
        'x_name': fields.char(
            'Makine Adi',
            size=128,
            required=False),
        'name': fields.char(
            'Makine Adi',
            size=128,
            required=False),
      
      }
x_makine()
class mrp_production(osv.Model):
    _inherit = 'mrp.production'
    _columns = {
        'x_operator': fields.many2one(
            'hr.employee',
            'Uretimi Yapan Operator'
            ),
        'x_note': fields.char(
            'Not',
            size=256,
            required=False),
        'x_makine': fields.many2one(
            'x_makine',
            'Uretim Yapilan Makine'
            ),
    }
mrp_production()
