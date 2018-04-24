from openerp.osv import osv, fields


class x_makine(osv.Model):
    _name = 'x.makine'
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
    
    def _get_procurement_group_name(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for mo in self.browse(cr, uid, ids, context=context):
            if mo.move_prod_id:
                res[mo.id] = mo.move_prod_id.group_id.name
            else:
                res[mo.id] = False
        return res
    
    
    def _get_product_route(self, cr, uid, ids, name, arg, context=None):
        def _get_route(move_id):
            if move_id:
                prev_route = _get_route(move_id.move_orig_ids)
                if prev_route:
                    return '|'.join([prev_route,move_id.location_dest_id.name])
                else:
                    return move_id.location_dest_id.name
            return False
        
        res = {}
        for mo in self.browse(cr, uid, ids, context=context):
            if mo.move_prod_id:
                res[mo.id] = _get_route(mo.move_prod_id)
            else:
                res[mo.id] = False
        return res
    
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
        'x_makine_kod': fields.related(
            'x_makine',
            'x_kod',
            type='char',
            string='Makine',
            readonly=1),
        'procurement_group_name': fields.function(
            _get_procurement_group_name, type='char', string="Procurement Group",
            readonly=True,
            ),
        'product_route': fields.function(
            _get_product_route, type='char', string="Product route",
            readonly=True,
            ),
    }
    
    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=80):
        if args is None:
            args = []
        if context is None:
            context = {}
        if name:
            args += [('move_prod_id.group_id.name', operator, name)]
        ids = self.search(cr, user, args, limit=limit, context=context)
        return self.name_get(cr, user, ids, context=context)

    
mrp_production()



