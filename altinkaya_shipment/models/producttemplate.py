from openerp.osv import fields, osv


class product_template(osv.osv):
    _inherit = 'product.template'

    def _default_route_ids(self):
        cr, uid = self._cr, self._uid,
        return self.pool.get('stock.location.route').search(cr, uid, [('name', '=', 'Manufacture')])


    _columns = {
        'route_ids': fields.many2many('stock.location.route', 'stock_route_product', 'product_id', 'route_id', 'Routes',
                                      domain="[('product_selectable', '=', True)]",
                                      default=_default_route_ids,
                                      help="Depending on the modules installed, this will allow you to define the route of the product: whether it will be bought, manufactured, MTO/MTS,..."),
    }



