# from openerp import api, fields, models, _

from openerp.osv import fields, osv


class res_partner_worksector(osv.osv):
    _name = 'worksector'

    _columns = {
        'description': fields.text(string="Description", translate=True),
        'name': fields.char(string="Name", translate=True),
        'partner_ids': fields.many2many('res.partner', 'table_worksector_partner_rel', 'wid', 'partid', string="Partner"),
        'product_categ_ids': fields.many2many('product.category', string="Category")
    }


class res_partner(osv.osv):
    _inherit = 'res.partner'

    def _get_product_categ(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        recids = self.browse(cr, uid, ids)
        for part in recids:
            lst = []
            for line in part.worksector_ids:
                lst += [x.id for x in line.product_categ_ids]
#             part.target_product_categ_ids = self.env['product.category'].browse(cr, uid, set(lst))
            res[part.id] = list(set(lst))
        return res

    _columns = {
        'worksector_ids': fields.many2many('worksector', 'table_worksector_partner_rel', 'partid', 'wid', string="Worksector"),
        'target_product_categ_ids': fields.function(_get_product_categ, type="many2many", relation='product.category', string="Target Product Category")
    }






# class worksector_line(models.Model):
#     _name = 'worksector.line'
# 
#     partner_id = fields.Many2one('res.partner', string="Partner")
#     worksector_id = fields.Many2one('worksector', string="worksector")


# class product_category_line(models.Model):
#     _name = 'product.category.line'
# 
#     product_categ_id = fields.Many2one('product.category', string="Product Category")
#     worksector_id = fields.Many2one('worksector', string="worksector")
