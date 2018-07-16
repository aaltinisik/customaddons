# -*- encoding: utf-8 -*-
#
#Created on Apr 2, 2018
#
#@author: dogan
#

from openerp import models, fields, api
import math


class MrpBoMWCParameter(models.Model):
    _name = 'mrp.bom.wcparameter'
    
    bom_id = fields.Many2one('mrp.bom',string='BoM')
    routing_wc_id = fields.Many2one('mrp.routing.workcenter','Workcenter')
    cycle_nbr = fields.Float('Cycle Number')
    hour_nbr = fields.Float('Cycle Time(Hour)')
    time_start = fields.Float('Time Before Prod.')
    time_stop = fields.Float('Time After Prod.')

class MrpBoM(models.Model):
    _inherit = 'mrp.bom'
    
    
    wc_parameter_ids = fields.One2many('mrp.bom.wcparameter','bom_id','Workcenter Parameters')

    categ_id = fields.Many2one('product.category',
                                 related='product_tmpl_id.categ_id',
                                 string='Category',
                                 store=True, readonly=True)

    @api.multi
    def _prepare_wc_line(self, wc_use, level=0, factor=1):
        res = super(MrpBoM, self)._prepare_wc_line(
            wc_use, level=level, factor=factor)
        
        cycle_by_bom = self.env['mrp.config.settings']._get_parameter(
            'cycle.by.bom')
        if not (cycle_by_bom and cycle_by_bom.value == 'True'):
            production = self.env.context.get('production')
            factor = self._factor(production and production.product_qty or 1,
                                  self.product_efficiency,
                                  self.product_rounding)
        
        wc_parameter_id = self.wc_parameter_ids.filtered(lambda wcp: wcp.routing_wc_id.id == wc_use.id)
        
        if len(wc_parameter_id) == 1:   
            
            cycle = wc_parameter_id.cycle_nbr or 1.0
            hour = wc_parameter_id.hour_nbr * cycle
            time_start = wc_parameter_id.time_start
            time_stop = wc_parameter_id.time_stop
            res.update({
                'cycle': cycle,
                'hour': hour,
                'time_start': time_start,
                'time_stop': time_stop
            })
        return res
    
    @api.multi
    @api.onchange('routing_id')
    def onchange_routing_id(self):
        res = super(MrpBoM, self).onchange_routing_id()
        
        self.wc_parameter_ids = False
        vals = []
        for wc_line in self.routing_id.workcenter_lines:
            default_wc_line = wc_line.op_wc_lines.filtered(lambda r: r.default)
            data_source = (default_wc_line if default_wc_line.custom_data else
                           default_wc_line.workcenter)
            
            vals.append( {'routing_wc_id':wc_line.id,
                    'cycle_nbr':wc_line.cycle_nbr,
                    'hour_nbr':wc_line.hour_nbr,
                    'time_start':data_source.time_start,
                    'time_stop':data_source.time_stop})

        
        self.wc_parameter_ids = [(0,False, val) for val in vals]
        
        return res

