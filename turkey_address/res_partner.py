from openerp.osv import osv, fields
import re

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
#                             'district_id':False,
#                             'region_id': False,
#                             'neighbour_id': False,
                             }}
        return {}

    def onchange_district(self, cr, uid, ids, district_id, context=None):
#        return {'value': {'region_id': False,'neighbour_id': False,}}
        return {}

    def onchange_region(self, cr, uid, ids, region_id, context=None):
#        return {'value': {'neighbour_id': False,}}
        return {}


    def onchange_neighbour(self, cr, uid, ids, neighbour_id, context=None):
        neighbour_obj = self.pool.get('address.neighbour')
        if neighbour_id:
            neighbour_rec = neighbour_obj.browse(cr, uid, neighbour_id, context=context)
            return {'value': {'zip': neighbour_rec and neighbour_rec.code,
                              'region_id':neighbour_rec and neighbour_rec.region_id,
                              'district_id': neighbour_rec and neighbour_rec.region_id.district_id,
                              'state_id': neighbour_rec and neighbour_rec.region_id.district_id.state_id,
                              'country_id': neighbour_rec and neighbour_rec.region_id.district_id.state_id.country_id,
                              }}
        return {'value': {}}

    def _display_address(self, cr, uid, address, without_company=False, context=None):

        '''
        The purpose of this function is to build and return an address formatted accordingly to the
        standards of the country where it belongs.

        :param address: browse record of the res.partner to format
        :returns: the address formatted in a display that fit its country habits (or the default ones
            if not country is specified)
        :rtype: string
        '''

        # get the information that will be injected into the display format
        # get the address format
        address_format = address.country_id.address_format or \
              "%(street)s\n%(street2)s\n%(city)s %(state_code)s %(zip)s\n%(country_name)s"
        args = {
            'state_code': address.state_id.code or '',
            'state_name': address.state_id.name or '',
            'country_code': address.country_id.code or '',
            'country_name': address.country_id.name or '',
            'company_name': address.parent_name or '',
            'neighbourhood_name': address.neighbour_id.name or '',
            'region_name': address.region_id.name or '',
            'district_name': address.district_id.name or '',

        }
        for field in self._address_fields(cr, uid, context=context):
            args[field] = getattr(address, field) or ''
        if without_company:
            args['company_name'] = ''
        elif address.parent_id:
            address_format = '%(company_name)s\n' + address_format
        display_address = address_format % args
        return re.sub('\n[\s,]*\n+', '\n', display_address.strip())
