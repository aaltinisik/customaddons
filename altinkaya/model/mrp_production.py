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
    
    def get_product_route(self):
        def _get_next_moves(move_id):
            if move_id:
                next_moves = _get_next_moves(move_id.move_dest_id)
                if next_moves:
                    return move_id | next_moves
                else:
                    return move_id
            return False
        
        res = {}
        #for mo in self.browse(cr, uid, ids, context=context):
        if self.move_prod_id:
            route = []
            for m in _get_next_moves(self.move_prod_id):
                if m.picking_id.id:
                    route.append(('picking',m.picking_id))
                elif m.raw_material_production_id.id:
                    route.append(('production',m.raw_material_production_id))
                
            res = route
        else:
            res = False
                
        return res

    
    def _get_product_pickings(self, cr, uid, ids, name, arg, context=None):
        def _get_next_moves(move_id):
            if move_id:
                next_moves = _get_next_moves(move_id.move_dest_id)
                if next_moves:
                    return move_id | next_moves
                else:
                    return move_id
            return False
        
        res = {}
        for mo in self.browse(cr, uid, ids, context=context):
            if mo.move_prod_id:
                res[mo.id] = _get_next_moves(mo.move_prod_id).mapped('picking_id')
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
        'product_pickings': fields.function(
            _get_product_pickings, type='many2many', string="Product Pickings", relation='stock.picking',
            readonly=True,
            )
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

#     def action_produce(self, cr, uid, production_id, production_qty, production_mode, wiz=False, context=None):
#         res = super(mrp_production, self).action_produce(cr, uid, production_id, production_qty, production_mode, wiz=wiz, context=context)
#         for production in self.browse(cr, uid, production_id):
#             for picking in production.product_pickings:
#                 picking.origin = '%s##%s##' % (picking.origin,production.name)
#         return res
    
    
mrp_production()



