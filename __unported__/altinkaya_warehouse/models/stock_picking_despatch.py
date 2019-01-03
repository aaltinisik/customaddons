# -*- encoding: utf-8 -*-
#
#Created on Oct 2, 2018
#
#@author: dogan
#

from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import ValidationError


class stock_picking(models.Model):
    _inherit = 'stock.picking'
    
    despatch_id = fields.Many2one('stock.picking.despatch', string='Carrier Despatch Document')
    

class stock_picking_despatch(models.Model):
    _name = 'stock.picking.despatch'
    _inherit = 'mail.thread'
    
    name = fields.Char('Number', default=_('New'), required=True, readonly=True)
    carrier_id = fields.Many2one('delivery.carrier',required=True, readonly=True, states={'draft': [('readonly', False)]})
    carrier_employee = fields.Char('Carrier Employee', readonly=True, states={'draft': [('readonly', False)]})
    picking_ids = fields.Many2many('stock.picking',string='Pickings', 
                                   relation='stock_picking_despatch_rel', column1='picking_id', column2='despatch_id', 
                                   readonly=True, states={'draft': [('readonly', False)]})
    date_done = fields.Datetime('Date Done', readonly=True)
    user_id = fields.Many2one('res.users','Dispatching User', readonly=True)
    state = fields.Selection([('draft','Draft'),
                              ('done','Delivered'),
                              ('cancel','Cancel')], track_visibility='onchange')
        
    
    @api.multi
    def action_done(self):
        self.ensure_one()
        self.write({'state':'done',
                    'user_id':self.env.user.id})
        
    @api.multi
    def action_cancel(self):
        self.ensure_one()
        self.picking_ids.write({'despatch_id':False})
        self.write({'state':'cancel'})
        
    @api.multi
    def action_draft(self):
        self.ensure_one()
        already_dispatched = self.picking_ids.filtered(lambda p: p.despatch_id.id)
        if len(already_dispatched) > 0:
            raise ValidationError('Already despatched pickings exist!\n%s' % '\n'.join(already_dispatched.mapped('name')))
        
        self.picking_ids.write({'despatch_id':self.id})
        self.write({'state':'draft'})
        
    @api.multi
    def action_print(self):
        return self.env['report'].with_context({'active_ids':self.ids}).get_action(self.ids,'altinkaya_warehouse.report_carrier_despatch')
    