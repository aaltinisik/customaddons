# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-TODAY Acespritech Solutions Pvt Ltd
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, _

class mrp_produce_more(models.TransientModel):
    _name = 'mrp.produce.more'


    def produce_mrp_order(self, cr, uid, ids, context=None):
        """ Cancels the production order and related stock moves.
        @return: True
        """
        if context is None:
            context = {}
        production_obj = self.pool.get('mrp.production')
        if context.get('active_ids'):
            production_ids = production_obj.search(cr, uid, [('id','in',context.get('active_ids')),
                                                             ('state','in',['confirmed','ready','in_production'])], 
                                                   context=context)
            for production in production_obj.browse(cr, uid, production_ids, context=context):
                if production.state == 'confirmed':
                    production_obj.action_assign(cr, uid, production.id, context=context)
                    production_obj.force_production(cr, uid, production.id)
                    result = production_obj._calculate_qty(cr, uid, production, product_qty=0.0, context=context)
                    line_ids = []
                    for ec in result:
                        line_ids.append(self.pool.get('mrp.product.produce.line').create(cr, uid, ec, context=context))
                    wizard_id = self.pool.get('mrp.product.produce').browse(cr, uid, self.pool.get('mrp.product.produce').create(cr, uid, {'mode':'consume_produce','product_qty':production.product_qty,
                                                                          'consume_lines':[(6,0,line_ids)]}), context=context)
                    production_obj.action_produce(cr, uid, production.id,
                                                  production.product_qty, 'consume_produce', wizard_id, context=context)
                elif production.state in ['ready','in_production']:
                    assert production.id, "Production Id should be specified in context as a Active ID."
                    result = production_obj._calculate_qty(cr, uid, production, product_qty=0.0, context=context)
                    line_ids = []
                    for ec in result:
                        line_ids.append(self.pool.get('mrp.product.produce.line').create(cr, uid, ec, context=context))
                    wizard_id = self.pool.get('mrp.product.produce').browse(cr, uid, self.pool.get('mrp.product.produce').create(cr, uid, {'mode':'consume_produce','product_qty':production.product_qty,
                                                                          'consume_lines':[(6,0,line_ids)]}), context=context)
                    production_obj.action_produce(cr, uid, production.id,
                            production.product_qty, 'consume_produce', wizard_id, context=context)
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
