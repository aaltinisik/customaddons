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
    state_id = fields.Many2one('res.country.state', 'State', related='district_id.state_id',store=True)

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
    state_id = fields.Many2one('res.country.state', 'State',  related='region_id.district_id.state_id',store=True)
    district_id = fields.Many2one('address.district', 'District',  related='region_id.district_id',store=True)

    def name_get2(self, cr, uid, ids, context=None):
        res = []
        for inst in self.browse(cr, uid, ids, context=context):
            name = inst.name or '/'
            if name and inst.district_id and inst.state_id:
                name=name+','+inst.district_id.name+','+inst.state_id.name
            res.append((inst.id, name))
        return res

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=80):
        if args is None:
            args = []
        if context is None:
            context = {}
        if name:
            args += [('name', operator, name)]
        if context.get('region_id'):
            args += [('region_id', '=', context.get('region_id'))]
        if context.get('state_id'):
            args += [('state_id', '=', context.get('state_id'))]
        ids = self.search(cr, user, args, limit=limit, context=context)
        return self.name_get2(cr, user, ids, context=context)
