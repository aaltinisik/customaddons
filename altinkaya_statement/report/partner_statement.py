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
from openerp.report import report_sxw
from openerp.osv import fields, osv
from openerp.tools.translate import _


class partner_statement(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(partner_statement, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'datetime': datetime,
            'get_statement_data' : self._get_statement_data,
        })

    def _get_statement_data(self,partner,data=None):
        statement_data = []
        balance, seq = 0.0, 0
        if partner.parent_id:
            raise osv.except_osv(_('User Error!'), _('You can not print this report for a Contact'))
        if data:
            end_date = parser.parse(data['date_end']).date()
            start_date = parser.parse(data['date_start']).date()
        else:
            end_date = date(date.today().year, 12, 31)
            start_date = date(date.today().year, 1, 1)
        move_type = ('receivable','payable')
        self.cr.execute('SELECT aj.name as journal, l.date_maturity as due_date, l.date, am.name, am.state, move_id, SUM(l.debit) AS debit, SUM(l.credit) AS credit FROM account_move_line AS l \
                        LEFT JOIN account_account a ON (l.account_id=a.id) \
                        LEFT JOIN account_move am ON (l.move_id=am.id) \
                        LEFT JOIN account_journal aj ON (am.journal_id=aj.id) \
                        WHERE (l.date BETWEEN %s AND %s) AND l.partner_id = '+ str(partner.commercial_partner_id.id) + 'AND  a.type IN ' + str(move_type) +
                         'GROUP BY aj.name,move_id,am.name,am.state,l.date,l.date_maturity \
                         ORDER BY l.date',(str(start_date),str(end_date)))
        for each_dict in self.cr.dictfetchall():
            seq += 1
            balance = (each_dict['debit'] - each_dict['credit']) + balance
            statement_data.append({
                'seq': seq,
                'number': each_dict['state'] == 'draft' and '*'+str(each_dict['move_id']) or each_dict['name'],
                'date': each_dict['date'] and datetime.strptime(each_dict['date'], '%Y-%m-%d').strftime('%d.%m.%Y') or False,
                'due_date': each_dict['due_date'] and datetime.strptime(each_dict['due_date'], '%Y-%m-%d').strftime('%d.%m.%Y') or False,
                'description': len(each_dict['journal']) >= 27 and each_dict['journal'][0:27] or each_dict['journal'],
                'debit': each_dict['debit'] or 0.0,
                'credit': each_dict['credit'] or 0.0,
                'balance': abs(balance) or 0.0,
                'dc': balance > 0.01 and 'B' or 'A',
                'total': balance or 0.0,
            })
        if not statement_data:
            raise osv.except_osv(_('User Error!'), _('No receivable or payable Move Lines for '+partner.name))
        return statement_data

report_sxw.report_sxw('report.partner.statement', 'res.partner',
                      'altinkaya_statement/report/partner_statement.rml',
                      parser=partner_statement, header="external")

report_sxw.report_sxw('report.partner.statement2', 'res.partner',
                      'altinkaya_statement/report/partner_statement2.rml',
                      parser=partner_statement, header="external")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
