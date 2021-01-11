# -*- coding: utf-8 -*-


from odoo import fields, models,api
from datetime import date,datetime


class WizarPartnerStatement(models.TransientModel):
    _name = "partner.statement.wizard"
    _description="Partner Statement Wizard"


    def _default_date_start(self):
        return date(date.today().year, 1, 1).strftime('%Y-%m-%d')
    def _default_date_end(self):
        return date(date.today().year, 12, 31).strftime('%Y-%m-%d')
    
    def _default_partner_ids(self):
        return self.env.context.get('active_ids')[0]
    
    date_start = fields.Date('Start Date', required=1,default=_default_date_start,store=True)
    date_end = fields.Date('End Date', required=1,default=_default_date_end,store=True)
    partner_id = fields.Many2one('res.partner',default=_default_partner_ids)
    
    
    @api.multi
    def print_report(self):
        data = {
            'ids': self.id,
            'doc_ids': self.id,
            'model': 'res.partner',
            'date_end':self.date_end,
            'date_start':self.date_start,
            'doc_model': self.env['res.partner']._name,
            'form': self.read()[0]}
        return self.env.ref('altinkaya_reports.partner_statement2_altinkaya'). \
            with_context(active_model='res.partner').report_action(docids=data['doc_ids'])
             
    
    @api.multi
    def _get_statement_data_currency(self,data=None):
        statement_data = []
        statement_dict = {}
        balance, seq = 0.0, 0
        Currency = self.env['res.currency']
        start_date=self.date_start
        partner= self.partner_id
        end_date =self.date_end
        move_type = ('payable','receivable')
        self.env.cr.execute('SELECT aj.name as journal, l.date_maturity as due_date, l.date, am.name, am.state, move_id, SUM(l.debit) AS debit, SUM(l.credit) AS credit,\
                        l.amount_currency as amount_currency,l.currency_id as currency_id,l.company_currency_id as company_currency_id\
                        FROM account_move_line AS l \
                        LEFT JOIN account_account a ON (l.account_id=a.id) \
                        LEFT JOIN account_move am ON (l.move_id=am.id) \
                        LEFT JOIN account_journal aj ON (am.journal_id=aj.id) \
                        LEFT JOIN account_account_type at ON (a.user_type_id =at.id) \
                        WHERE (l.date BETWEEN %s AND %s) AND l.partner_id = '+ str(partner.commercial_partner_id.id) + ' AND  at.type IN ' + str(move_type) +
                        'GROUP BY aj.name,move_id,am.name,am.state,l.date,l.date_maturity ,l.amount_currency,l.currency_id,l.company_currency_id\
                         ORDER BY l.date , l.currency_id ',(str(start_date),str(end_date)))
        for each_dict in self.env.cr.dictfetchall():
#             if each_dict['currency_id'] and each_dict['amount_currency'] :
            seq += 1
             
            debit = 0.0
            credit = 0.0
            if each_dict['currency_id'] and each_dict['amount_currency'] :
                if  (each_dict['debit'] - each_dict['credit']) > 0.0:
                    debit = (each_dict['amount_currency'] - each_dict['credit'])
#                     balance = (each_dict['amount_currency'] - each_dict['credit']) + balance
                else:
                    credit = (each_dict['credit'] - each_dict['amount_currency'])
#                     balance = (each_dict['debit'] - each_dict['amount_currency']) + balance
                currency_id =   Currency.browse( each_dict['currency_id'])  
            else:
                if  (each_dict['debit'] - each_dict['credit']) > 0.0:
                    debit = (each_dict['debit'] - each_dict['credit'])
                else:
                    credit = (each_dict['credit'] - each_dict['debit'])        
#                 balance = (each_dict['debit'] - each_dict['credit']) + balance
                currency_id =   Currency.browse( each_dict['company_currency_id'])  
                
                
                
                
            statement_data.append({
                'seq': seq,
                'number': each_dict['state'] == 'draft' and '*'+str(each_dict['move_id']) or each_dict['name'],
                'date': each_dict['date'] and datetime.strptime(str(each_dict['date']), '%Y-%m-%d').strftime('%d.%m.%Y') or False,
                'due_date': each_dict['due_date'] and datetime.strptime(str(each_dict['due_date']), '%Y-%m-%d').strftime('%d.%m.%Y') or False,
                'description': len(each_dict['journal']) >= 30 and each_dict['journal'][0:30] or each_dict['journal'],
                'debit': debit,
                'credit': credit,
                'balance': abs(balance) or 0.0,
                'dc': balance > 0.01 and 'D' or 'C',
                'total': balance or 0.0,
                'currency_id': currency_id ,
            })
        
        for s in  statement_data:
            if not  s['currency_id'] in statement_dict:
                statement_dict[s['currency_id']] = []
            
            statement_dict[s['currency_id'] ].append(s)
            
            
        for currency  in statement_dict:
            balance = 0.0
            for s in statement_dict[currency]:
                balance = (s['debit'] - s['credit']) + balance
                s.update({
                     'balance' :  abs(balance) or 0.0,
                     'dc' : balance > 0.01 and 'D' or 'C',
                    
                    })    
                
        return statement_dict
    
    
    
            
    @api.multi
    def get_statement_data(self,data=None):
        statement_data = []
        balance, seq = 0.0, 0
        statement_dict = {}
        start_date=self.date_start
        partner= self.partner_id
        end_date =self.date_end
        Currency = self.env['res.currency']
        move_type = ('payable','receivable')
        self.env.cr.execute('SELECT aj.name as journal, l.date_maturity as due_date, l.date, am.name, am.state, move_id, SUM(l.debit) AS debit, SUM(l.credit) AS credit,\
                        l.amount_currency as amount_currency,l.currency_id as currency_id,l.company_currency_id as company_currency_id\
                        FROM account_move_line AS l \
                        LEFT JOIN account_account a ON (l.account_id=a.id) \
                        LEFT JOIN account_move am ON (l.move_id=am.id) \
                        LEFT JOIN account_journal aj ON (am.journal_id=aj.id) \
                        LEFT JOIN account_account_type at ON (a.user_type_id =at.id) \
                        WHERE (l.date BETWEEN %s AND %s) AND l.partner_id = '+ str(partner.commercial_partner_id.id) + ' AND  at.type IN ' + str(move_type) +
                        'GROUP BY aj.name,move_id,am.name,am.state,l.date,l.date_maturity ,l.amount_currency,l.currency_id,l.company_currency_id\
                         ORDER BY l.date , l.currency_id ',(str(start_date),str(end_date)))
        for each_dict in self.env.cr.dictfetchall():
            seq += 1
            balance = (each_dict['debit'] - each_dict['credit']) + balance
            debit = 0.0
            credit = 0.0
            currency_id = Currency.browse(each_dict['company_currency_id'])
            if  (each_dict['debit'] - each_dict['credit']) > 0.0:
                debit = (each_dict['debit'] - each_dict['credit'])
            else:
                credit = (each_dict['credit'] - each_dict['debit'])

            statement_data.append({
                'seq': seq,
                'number': each_dict['state'] == 'draft' and '*'+str(each_dict['move_id']) or each_dict['name'],
                'date': each_dict['date'] and datetime.strptime(str(each_dict['date']), '%Y-%m-%d').strftime('%d.%m.%Y') or False,
                'due_date': each_dict['due_date'] and datetime.strptime(str(each_dict['due_date']), '%Y-%m-%d').strftime('%d.%m.%Y') or False,
                'description': len(each_dict['journal']) >= 30 and each_dict['journal'][0:30] or each_dict['journal'],
                'debit': debit,
                'credit': credit,
                'balance': abs(balance) or 0.0,
                'dc': balance > 0.01 and 'B' or 'A',
                'total': balance or 0.0,
                'currency_symbol': currency_id['symbol'],
            })
        return statement_data
    

