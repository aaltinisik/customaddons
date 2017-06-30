from openerp.osv import osv, fields


#class res_partner(models.Model):
#    _inherit = 'res.partner'
#
#    district_id = fields.Many2one('address.district', string='District')
#    region_id = fields.Many2one('address.region', string='Region')
#    neighbour_id = fields.Many2one('address.neighbour', string='Neighbourhood')

class res_partner(osv.osv):
    _inherit = "res.partner"

    _columns = {

        'district_id': fields.many2one('address.district', 'District'),
        'region_id': fields.many2one('address.region', 'Region'),
        'neigbour_id': fields.many2one('address.neigbour', 'Neighbourhood'),
    }

res_partner()
