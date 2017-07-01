from openerp import models, fields, api


class region_district(models.Model):
    _name = 'address.district'

    name = fields.Char(string='District')
    state_id = fields.Many2one('res.country.state', 'State', required=True)

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
    district_id = fields.Many2one('address.district', 'District', required=True)

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


class addres_neighbour(models.Model):
    _name = 'address.neighbour'

    name = fields.Char(string='Neighbour')
    region_id = fields.Many2one('address.region', 'Region', required=True)
    code = fields.Char('Postal Code')


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

class res_partner(models.Model):
    _inherit = 'res.partner'

    district_id = fields.Many2one('address.district', string='District')
    region_id = fields.Many2one('address.region', string='Region')
    neighbour_id = fields.Many2one('address.neighbour', string='Neighbourhood')

    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            district = self.env['address.district'].search([('state_id', '=', state_id)], limit=1)
            print '::district', district and district.id
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id,
                              'district_id': district and district.id}}
        return {'value': {}}

    @api.multi
    def onchange_district(self, district_id):
        if district_id:
            region = self.env['address.region'].search([('district_id', '=', district_id)], limit=1)
            return {'value': {'region_id': region and region.id}}
        return {'value': {}}

    @api.multi
    def onchange_region(self, region_id):
        if region_id:
            neighbour = self.env['address.neighbour'].search([('region_id', '=', region_id)], limit=1)
#            code = (neighbour and neighbour.code) or self._context.get('zip')
            return {'value': {'neighbour_id': neighbour and neighbour.id,
                              }}
        return {'value': {}}

    @api.multi
    def onchange_neighbour(self, neighbour_id):
        if neighbour_id:
            neighbour = self.env['address.neighbour'].search([('neighbour_id', '=', neighbour_id)], limit=1)
           # code = (neighbour and neighbour.code) or self._context.get('zip')
            return {'value': {'zip': neighbour and neighbour.code}}
        return {'value': {}}

