from openerp import tools, api, SUPERUSER_ID
from openerp.osv import osv, fields

class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'district_id': fields.many2one('address.district', string='District'),
        'region_id': fields.many2one('address.region', string='Region'),
        'neighbour_id': fields.many2one('address.neighbour', string='Neighbourhood'),
    }

    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            district = self.env['address.district'].search([('state_id', '=', state_id)], limit=1)
            print '::district', district
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id,
                              'district_id': district and district.id}}
        return {'value': {}}

    def onchange_district(self, cr, uid, ids, district_id, context=None):
        region_obj = self.pool.get('address.region')
        if district_id:
            region_ids = region_obj.search(cr, uid, [('district_id', '=', district_id)], limit=1, context=context)
            region_rec = region_obj.browse(cr, uid, region_ids, context=context)
            return {'value': {'region_id': region_rec and region_rec.id}}
        return {'value': {}}

    def onchange_region(self, cr, uid, ids, region_id, context=None):
        neighbour_obj = self.pool.get('address.neighbour')
        if region_id:
            neighbour_ids = neighbour_obj.search(cr, uid, [('region_id', '=', region_id)], limit=1, context=context)
            neighbour_rec = neighbour_obj.browse(cr, uid, neighbour_ids, context)
            return {'value': {'neighbour_id': neighbour_rec and neighbour_rec.id,
                              }}
        return {'value': {}}

    def onchange_neighbour(self, cr, uid, ids, neighbour_id, context=None):
        neighbour_obj = self.pool.get('address.neighbour')
        if neighbour_id:
            neighbour_rec = neighbour_obj.browse(cr, uid, neighbour_id, context=context)
            return {'value': {'zip': neighbour_rec and neighbour_rec.code}}
        return {'value': {}}

