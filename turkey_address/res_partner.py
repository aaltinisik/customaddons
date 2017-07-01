from openerp.osv import osv, fields

class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'district_id': fields.many2one('address.district', string='District'),
        'region_id': fields.many2one('address.region', string='Region'),
        'neighbour_id': fields.many2one('address.neighbour', string='Neighbourhood'),
    }

    def onchange_state(self, cr, uid, ids, state_id, context=None):
        if state_id:
            country_id=self.pool.get('res.country.state').browse(cr, uid, state_id, context).country_id.id
            return {'value':{'country_id':country_id,
                             'district_id':False,
                             'region_id': False,
                             'neighbour_id': False,
                             }}
        return {}

    def onchange_district(self, cr, uid, ids, district_id, context=None):
        return {'value': {'region_id': False,'neighbour_id': False,}}


    def onchange_region(self, cr, uid, ids, region_id, context=None):
        return {'value': {'neighbour_id': False,}}

    def onchange_neighbour(self, cr, uid, ids, neighbour_id, context=None):
        neighbour_obj = self.pool.get('address.neighbour')
        if neighbour_id:
            neighbour_rec = neighbour_obj.browse(cr, uid, neighbour_id, context=context)
            return {'value': {'zip': neighbour_rec and neighbour_rec.code}}
        return {'value': {}}

