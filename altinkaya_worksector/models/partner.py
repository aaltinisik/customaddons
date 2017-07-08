from openerp.osv import osv, fields

class res_partner_worksector(osv.osv):
    _name = 'res.partner.worksector'

    _columns = {
        'description' : fields.text(string="Description", translate=True),
        'name' : fields.char(string="Name", translate=True),
        'partner_ids' : fields.one2many('worksector.line', 'worksector_id', string="Partner"),
        'product_categ_ids' : fields.one2many('product.category.line', 'worksector_id', string="Category"),
    }


class res_partner(osv.osv):
    _inherit = 'res.partner'

    def _get_product_categ(self, cr, uid, ids, name, args, context=None):
        res = {}
        for part in self.browse(cr, uid, ids, context=context):
            lst = []
            for line in part.worksector_ids:
                lst += [x.product_categ_id.id for x in line.worksector_id.product_categ_ids]
            res[part.id] = lst
        return res

    _columns = {
        'worksector_ids' : fields.one2many('worksector.line', 'partner_id', string="Worksector"),
        'target_product_categ_ids' : fields.function(_get_product_categ, string='Entry Lines', type='many2many', relation='product.category'),
    }


class worksector_line(osv.osv):
    _name = 'worksector.line'

    _columns = {
        'partner_id' : fields.many2one('res.partner', string="Partner"),
        'worksector_id' : fields.many2one('res.partner.worksector', string="worksector"),
    }


class product_category_line(osv.osv):
    _name = 'product.category.line'

    _columns = {
        'product_categ_id' : fields.many2one('product.category', string="Product Category"),
        'worksector_id' : fields.many2one('res.partner.worksector', string="worksector"),
    }
