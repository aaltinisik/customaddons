# -*- encoding: utf-8 -*-
#
#Created on Dec 4, 2018
#
#@author: dogan
#

from openerp import models, fields, api, _


class PartnerReconcileClose(models.TransientModel):
    """
    Wizard for reconciliation of account move lines and creating closing/opening moves
    """
    _name = 'partner.reconcile.close'
    
    
    country_id = fields.Many2one('res.country',string='Partner Country')
    customer = fields.Boolean('Customer')
    supplier = fields.Boolean('Supplier')
    partner_id = fields.Many2one('res.partner',string='Partner')
    transfer_journal_id = fields.Many2one('account.journal', string='Transfer Journal', required=True)
    transfer_account_id = fields.Many2one('account.account', string='Transfer Account', required=True)
    transfer_description = fields.Char('Transfer description', required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    opening_period_id = fields.Many2one('account.period', string='Opening Period', required=True)
    opening_move_date = fields.Date('Opening Move Date', required=True)
    closing_period_id = fields.Many2one('account.period', string='Closing Period', required=True)
    closing_move_date = fields.Date('Closing Move Date', required=True)
    
    
    @api.onchange('opening_period_id')
    def onchange_opening_period_id(self):
        self.opening_move_date = self.opening_period_id.date_start
    
    @api.onchange('closing_period_id')
    def onchange_closing_period_id(self):
        self.closing_move_date = self.closing_period_id.date_stop
    
    
    @api.onchange('country_id','customer','supplier')
    def onchange_country_id(self):
        domain = []
        if self.country_id:
            domain.append(('country_id','=',self.country_id.id))
            
        if self.customer and not self.supplier:
            domain.append(('customer','=',True))
            
        if not self.customer and self.supplier:
            domain.append(('supplier','=',True))
        
        if self.customer and self.supplier:
            domain.extend(['|',('customer','=',True),('supplier','=',True)])
        
        return {'domain':{'partner_id':domain}}
    
    
    @api.multi
    def action_done(self):
        
        self.ensure_one()
        domain = [('date','>=',self.start_date),('date','<=',self.end_date)]
        partner_ids = self.env['res.partner']
        move_obj = self.env['account.move']
        move_line_obj = self.env['account.move.line'].with_context({'comment':self.transfer_description})
        if self.partner_id:
            partner_ids |= self.partner_id
        else:
            partner_domain = []
            
            if self.country_id:
                partner_domain.append(('country_id','=',self.country_id.id))
                
            if self.customer and not self.supplier:
                partner_domain.append(('customer','=',True))
                
            if not self.customer and self.supplier:
                partner_domain.append(('supplier','=',True))
            
            if self.customer and self.supplier:
                partner_domain.extend(['|',('customer','=',True),('supplier','=',True)])
            
            partner_ids = self.env['res.partner'].search(partner_domain)
            
    
        closing_lines = []
        opening_lines = []
        for partner in partner_ids:
            for account in [partner.property_account_receivable, partner.property_account_payable]:
            
                lines = move_line_obj.search(domain + [('partner_id','=',partner.id),('account_id','=',account.id)])   
                balance = sum([ ml.debit - ml.credit for ml in lines])
                
                if balance > 0:
                    debit = balance
                    credit = 0.0
                    self_credit = balance
                    self_debit = 0.0
                elif balance < 0:
                    debit = 0.0
                    credit = -balance
                    self_credit = 0.0
                    self_debit = -balance
                else:
                    continue
                
                closing_lines.extend([
                                        (0, 0, {
                                            'name': _('Closing'),
                                            'debit': self_debit,
                                            'credit': self_credit,
                                            'account_id': account.id,
                                            'date': self.closing_move_date,
                                            'partner_id': partner.id,
                                            'currency_id': (account.currency_id.id or False)
                                        }),
                                        (0, 0, {
                                            'name': _('Closing'),
                                            'debit': debit,
                                            'credit': credit,
                                            'account_id': self.transfer_account_id.id,
                                            'date': self.closing_move_date,
                                            'partner_id': partner.id,
                                            'currency_id': (account.currency_id.id or False)
                                        })
                                      ])
                
                opening_lines.extend([
                                        (0, 0, {
                                            'name': _('Opening'),
                                            'debit': debit,
                                            'credit': credit,
                                            'account_id': account.id,
                                            'date': self.opening_move_date,
                                            'partner_id': partner.id,
                                        }),
                                        (0, 0, {
                                            'name': _('Opening'),
                                            'debit': self_debit,
                                            'credit': self_credit,
                                            'account_id': self.transfer_account_id.id,
                                            'date': self.opening_move_date,
                                            'partner_id': partner.id,
                                        })
                                      ])
            
                
            
        closing_move_id = move_obj.create({
            'period_id': self.closing_period_id.id,
            'journal_id': self.transfer_journal_id.id,
            'date':self.closing_move_date,
            'state': '',
            'line_id': closing_lines
        })
        
        opening_move_id = move_obj.create({
            'period_id': self.opening_period_id.id,
            'journal_id': self.transfer_journal_id.id,
            'date':self.opening_move_date,
            'state': 'draft',
            'line_id': opening_lines
        })
        
        
        closing_move_id.post()
        opening_move_id.post()
        
        for partner in partner_ids:
            for account in [partner.property_account_receivable, partner.property_account_payable]:
                lines = move_line_obj.search(domain + [('partner_id','=',partner.id),('account_id','=',account.id)])   
                lines |= closing_move_id.line_id.filtered(lambda ml: ml.account_id.id == account.id and ml.partner_id.id == partner.id)
                move_line_obj._remove_move_reconcile(lines.ids)
                lines.reconcile()
                
            lines = closing_move_id.line_id.filtered(lambda ml: ml.account_id.id == self.transfer_account_id.id and ml.partner_id.id == partner.id)
            lines |= opening_move_id.line_id.filtered(lambda ml: ml.account_id.id == self.transfer_account_id.id and ml.partner_id.id == partner.id)
            lines.reconcile()

        
        
        return {
            'name': _('Account Moves'),
            'view_type':'form',
            'view_mode':'tree',
            'res_model':'account.move',
            'view_id':False,
            'type':'ir.actions.act_window',
            'domain':[('id','in',[opening_move_id.id, closing_move_id.id])],
            'context':self._context
        }
        
        
                
                
                
                
                
            
            

            
        
            
        
        
    
    