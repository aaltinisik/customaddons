# -*- encoding: utf-8 -*-
#
#Created on Dec 18, 2018
#
#@author: dogan
#

from openerp import models, api, fields


class stock_quant(models.Model):
    _inherit = 'stock.quant'

    ignore_reservation = fields.Boolean(related='location_id.ignore_reservation',store=True)
    priority = fields.Integer(related='location_id.priority', help='high priority quants will be reserved first',
                             readonly=True, store=True)

    @api.model
    def _quants_get_order(self, location, product, quantity, domain=[], orderby='in_date'):
        ''' overwrite default behavior
        '''
        def check_ignore_disable(domain):

            for node in domain:
                if isinstance(node,tuple):
                    if node[0] == 'history_ids':
                        return True
            return False


        if  not check_ignore_disable(domain) and location and not location.ignore_reservation:
                domain += [('ignore_reservation','=',False)]

        return super(stock_quant, self)._quants_get_order(location=location, product=product, quantity=quantity,
                                                                  domain=domain, orderby='priority, %s' % orderby)
    
    @api.model
    def search(self, domain, *args, **kwargs):
        for i, e in enumerate(domain):
            if not isinstance(e, basestring) and e[0] == 'multi_location':
                self.env.cr.execute(
                """select id, location_id from (
                        select p.id, l.location_id, count(distinct q.location_id) as c from stock_quant q 
                            join product_product p on q.product_id = p.id 
                            join stock_location l on l.id = q.location_id 
                        where l.usage = 'internal' and l.active = true
                        group by p.id, l.location_id order by p.id
                    ) res  where res.c > 1 """,
                log_exceptions=False)
                res = self.env.cr.fetchall()
                domain[i] = ('location_id', 'child_of', list(set([r[1] for r in res]))) 
                domain.insert(i,('product_id','in',list(set([r[0] for r in res]))))
                
        return super(stock_quant, self).search(domain, *args, **kwargs)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        for i, e in enumerate(domain):
            if not isinstance(e, basestring) and e[0] == 'multi_location':
                self.env.cr.execute(
                """select id, location_id from (
                        select p.id, l.location_id, count(distinct q.location_id) as c from stock_quant q 
                            join product_product p on q.product_id = p.id 
                            join stock_location l on l.id = q.location_id 
                        where l.usage = 'internal' and l.active = true
                        group by p.id, l.location_id order by p.id
                    ) res  where res.c > 1 """,
                log_exceptions=False)
                res = self.env.cr.fetchall()
                domain[i] = ('location_id', 'child_of', list(set([r[1] for r in res]))) 
                domain.insert(i,('product_id','in',list(set([r[0] for r in res]))))
        
        res = super(stock_quant, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        return res
