# -*- encoding: utf-8 -*-
#
#Created on Dec 27, 2018
#
#@author: dogan
#

from openerp import api
from openerp.osv import osv, fields


class Report(osv.Model):
    _inherit = 'report'
    
    
    def render(self, cr, uid, ids, template, values=None, context=None):
        if values['doc_model'] == 'stock.picking':
            values['docs'].filtered(lambda p: p.state in ['confirmed','waiting']).action_assign()
            
        return super(Report, self).render(cr, uid, ids, template, values=values, context=context)
    