# from openerp import api, fields, models, _
from openerp.osv import osv, fields

class res_partner_worksector(osv.osv):
    _name = 'res.partner.worksector'

    _columns = {
        'description' : fields.text(string="Description", translate=True),
        'name' : fields.char(string="Name", translate=True),
        'partner_ids' : fields.one2many('worksector.line', 'worksector_id', string="Partner"),
        'product_categ_ids' : fields.one2many('product.category.line', 'worksector_id', string="Category"),
#        'product_categ_ids': fields.many2many('product.category.line', 'partner_sector_prod_categ_line_rel', 'partner_wrksector_id', 'categ_line_id', string="Category")
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
#        'worksector_ids' : fields.one2many('worksector.line', 'partner_id', string="Worksector"),
        'worksector_ids' : fields.many2many('worksector.line', 'partner_work_sector_line_rel', 'partner_id', 'work_sector_line_id', string="Worksector"),
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


class product_category(osv.osv):
    _inherit = 'product.category'

    _columns = {
        'product_categ_id': fields.many2one('product.category', string="Product Category"),
#        'product_category_ids': fields.one2many('product.category', 'product_categ_id', string="Categories")
        'product_category_ids': fields.many2many('product.category', 'prod_categ_rel', 'partner_wrksector_id', 'categ_id', string="Categories")
    }