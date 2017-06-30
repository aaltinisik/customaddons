from openerp.osv import osv, fields

class res_partner(osv.osv):
    _inherit = "res.partner"

    _columns = {

        'district_id': fields.many2one('address.district', 'District'),
        'region_id': fields.many2one('address.region', 'Region'),
        'neighbour_id': fields.many2one('address.neighbour', 'Neighbourhood'),
    }

res_partner()
