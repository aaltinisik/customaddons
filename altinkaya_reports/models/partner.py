# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

import time
from datetime import date,datetime
from dateutil import parser
from odoo import models, fields,api
from odoo.tools.translate import _


class Partner(models.Model):
    _inherit='res.partner'

    # use_secondary_currency = fields.Boolean(string="Ekstrede çift para birimi yazdır",default=False)
    
    @api.multi
    def _get_statement_data_currency(self,data=None):
        statement_data = []
        statement_dict = {}
        balance, seq = 0.0, 0
        Currency = self.env['res.currency']
        end_date = date(date.today().year, 12, 31)
        start_date = date(1985, 1, 1)
        move_type = ('payable','receivable')
        self.env.cr.execute('SELECT aj.name as journal, l.date_maturity as due_date, l.date, am.name, am.state, move_id, SUM(l.debit) AS debit, SUM(l.credit) AS credit,\
                        l.amount_currency as amount_currency,l.currency_id as currency_id,l.company_currency_id as company_currency_id\
                        FROM account_move_line AS l \
                        LEFT JOIN account_account a ON (l.account_id=a.id) \
                        LEFT JOIN account_move am ON (l.move_id=am.id) \
                        LEFT JOIN account_journal aj ON (am.journal_id=aj.id) \
                        LEFT JOIN account_account_type at ON (a.user_type_id =at.id) \
                        WHERE (l.date BETWEEN %s AND %s) AND l.partner_id = '+ str(self.commercial_partner_id.id) + ' AND  at.type IN ' + str(move_type) +
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
    def _get_statement_data(self,data=None):
        statement_data = []
        balance, seq = 0.0, 0
        Currency = self.env['res.currency']
        end_date = date(date.today().year, 12, 31)
        start_date = date(date.today().year, 1, 1)
        move_type = ('payable','receivable')
        self.env.cr.execute('SELECT aj.name as journal, l.date_maturity as due_date, l.date, am.name, am.state, move_id, SUM(l.debit) AS debit, SUM(l.credit) AS credit,\
                                l.amount_currency as amount_currency,l.currency_id as currency_id,l.company_currency_id as company_currency_id\
                                FROM account_move_line AS l \
                                LEFT JOIN account_account a ON (l.account_id=a.id) \
                                LEFT JOIN account_move am ON (l.move_id=am.id) \
                                LEFT JOIN account_journal aj ON (am.journal_id=aj.id) \
                                LEFT JOIN account_account_type at ON (a.user_type_id =at.id) \
                                WHERE (l.date BETWEEN %s AND %s) AND l.partner_id = ' + str(self.commercial_partner_id.id) + ' AND  at.type IN ' + str(move_type) +
                            'GROUP BY aj.name,move_id,am.name,am.state,l.date,l.date_maturity ,l.amount_currency,l.currency_id,l.company_currency_id\
                             ORDER BY l.date , l.currency_id ', (str(start_date), str(end_date)))
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
    
    def email_statement(self,):
        data_model = self.env['ir.model.data']
        template = data_model.get_object('altinkaya_reports', 'email_template_edi_send_statement')
        mail_id = template.send_mail( self.id, force_send=True)
        return True
