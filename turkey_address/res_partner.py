from openerp import models, fields, api
#from openerp.osv import osv, fields

class address_district(models.Model):
    _name = 'address.district'

    name = fields.Char(string='District')
    state_id = fields.Many2one('res.country.state', 'State')

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=80):
        if args is None:
            args = []
        if context is None:
            context = {}
        if name:
            args += [('name', operator, name)]
        if context.get('state_id'):
            args += [('state_id', '=', context.get('state_id'))]
        ids = self.search(cr, user, args, limit=limit, context=context)
        return self.name_get(cr, user, ids, context=context)


class address_region(models.Model):
    _name = 'address.region'

    name = fields.Char(string='Region')
    district_id = fields.Many2one('address.district', 'District')

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=80):
        if args is None:
            args = []
        if context is None:
            context = {}
        if name:
            args += [('name', operator, name)]
        if context.get('district_id'):
            args += [('district_id', '=', context.get('district_id'))]
        ids = self.search(cr, user, args, limit=limit, context=context)
        return self.name_get(cr, user, ids, context=context)


class addres_neigbour(models.Model):
    _name = 'address.neigbour'

    name = fields.Char(string='Neigbourhood')
    region_id = fields.Many2one('address.region', 'Region')


    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=80):
        if args is None:
            args = []
        if context is None:
            context = {}
        if name:
            args += [('name', operator, name)]
        if context.get('region_id'):
            args += [('region_id', '=', context.get('region_id'))]
        ids = self.search(cr, user, args, limit=limit, context=context)
        return self.name_get(cr, user, ids, context=context)

#class res_partner(models.Model):
#    _inherit = 'res.partner'
#
#    district_id = fields.Many2one('address.district', string='District')
#    region_id = fields.Many2one('address.region', string='Region')
#    neighbour_id = fields.Many2one('address.neighbour', string='Neighbourhood')

# class res_partner(osv.osv):
#     _inherit = "res.partner"
#
#     _columns = {
#
#         'district_id': fields.many2one('address.district', 'District'),
#         'region_id': fields.many2one('address.region', 'Region'),
#         'neigbour_id': fields.many2one('address.neigbour', 'Neighbourhood'),
#     }
#
# res_partner()
