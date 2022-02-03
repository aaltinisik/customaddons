# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today Acespritech Solutions Pvt Ltd
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
from openerp.osv import fields,osv
from openerp.tools.translate import _
import time
from StringIO import StringIO
import xlwt
import base64
from datetime import date, datetime
from dateutil import parser


class wizard_partner_doviz_statement(osv.osv_memory):
    _name = "wizard.partner.doviz.statement"
    _columns = {
        'start_date': fields.date('Başlangıç Tarihi', required=True),
        'end_date': fields.date('Bitiş Tarihi', required=True),
        'partner_id': fields.many2one('res.partner', 'Cari') # , default=lambda self: self.env.user.partner_id
    }
    _defaults ={
        'start_date': lambda *a: time.strftime('%Y-01-01'),
        'end_date': lambda *a: time.strftime('%Y-%m-%d'),
        'partner_id': lambda self, cr, uid, context: context.get('partner_id', False),
    }

    def print_report(self, cr, uid, ids, context=None):
        xlsx_file = self._set_template(cr, uid, ids, context)

        ctx = dict(context)
        ctx.update({'file': xlsx_file})
        form_id = self.pool.get('ir.model.data').get_object_reference(cr, uid,'partner_doviz_statement',
                                                                      'customer_statement_excel_form')[1]
        return {
           'type': 'ir.actions.act_window',
           'view_type': 'form',
           'view_mode': 'form',
           'res_model': 'customer.statement.excel',
           'views': [(form_id, 'form')],
           'view_id': form_id,
           'target': 'new',
           'context': ctx,
        }

    def _get_statement_data(self, cr, partner, data=None):
        statement_data = []
        balance, sec_curr_balance, seq = 0.00, 0.00, 0
#        if partner.parent_id:
#            raise osv.except_osv(_('User Error!'), _('You can not print this report for a Contact'))
        if data:
            end_date = parser.parse(data['date_end']).date()
            start_date = parser.parse(data['date_start']).date()
        else:
            end_date = date(date.today().year, 12, 31)
            if date.today().month < 4:
                start_date = date(date.today().year-1, 1, 1)
            else:
                start_date = date(date.today().year, 1, 1)
        move_type = ('receivable','payable')
        cr.execute('SELECT aj.name as journal, l.date_maturity as due_date, l.date, am.name, am.state, move_id, SUM(l.debit) AS debit, SUM(l.credit) AS credit FROM account_move_line AS l \
                        LEFT JOIN account_account a ON (l.account_id=a.id) \
                        LEFT JOIN account_move am ON (l.move_id=am.id) \
                        LEFT JOIN account_journal aj ON (am.journal_id=aj.id) \
                        WHERE (l.date BETWEEN %s AND %s) AND l.partner_id = '+ str(partner.commercial_partner_id.id) + 'AND  a.type IN ' + str(move_type) +
                         'GROUP BY aj.name,move_id,am.name,am.state,l.date,l.date_maturity \
                         ORDER BY l.date',(str(start_date),str(end_date)))
        for each_dict in cr.dictfetchall():
            seq += 1
            balance = round((each_dict['debit'] - each_dict['credit']) + balance, 2)
            debit = 0.00
            credit = 0.00
            sec_curr_debit = 0.00
            sec_curr_credit = 0.00

            if (each_dict['debit'] - each_dict['credit']) > 0.00:
                debit = (each_dict['debit'] - each_dict['credit'])
            else:
                credit = (each_dict['credit'] - each_dict['debit'])

            if partner.has_secondary_curr:
                move_date = datetime.strptime(each_dict['date'], '%Y-%m-%d')
                cr.execute(
                        "SELECT rate\
                            FROM res_currency_rate\
                        WHERE currency_id = %s\
                        AND name <= %s\
                        ORDER BY name desc LIMIT 1", (partner.secondary_curr_id.id, move_date))
                if cr.rowcount:
                    rate = cr.fetchall()[0][0]
                else:
                    rate = 1.00

                sec_curr_debit = debit * rate
                sec_curr_credit = credit * rate
                sec_curr_balance = (sec_curr_debit - sec_curr_credit) + sec_curr_balance

            statement_data.append({
                'seq': seq,
                'number': each_dict['state'] == 'draft' and '*'+str(each_dict['move_id']) or each_dict['name'],
                'date': each_dict['date'] and datetime.strptime(each_dict['date'], '%Y-%m-%d').strftime('%d.%m.%Y') or False,
                'due_date': each_dict['due_date'] and datetime.strptime(each_dict['due_date'], '%Y-%m-%d').strftime('%d.%m.%Y') or False,
                'description': len(each_dict['journal']) >= 30 and each_dict['journal'][0:30] or each_dict['journal'],
                'debit': debit,
                'credit': credit,
                'balance': abs(balance) or 0.00,
                'sec_curr_debit': sec_curr_debit,
                'sec_curr_credit': sec_curr_credit,
                'sec_curr_balance': abs(sec_curr_balance) or 0.00,
                'sec_curr_dc': sec_curr_balance > 0.01 and 'B' or 'A',
                'dc': balance > 0.01 and 'B' or 'A',
                'sec_curr_total': sec_curr_balance or 0.00,
                'total': balance or 0.00,
            })
        return partner.secondary_curr_id, statement_data

    def _set_template(self, cr, uid, ids, context):
        record = self.browse(cr, uid, ids[0], context=context)
        second_currency, data = self._get_statement_data(cr, record.partner_id, data={'date_start': record.start_date,
                                                                                        'date_end': record.end_date})
        fl = StringIO()
        wbk = xlwt.Workbook()

        # styles

        header_style = xlwt.easyxf('font: bold on; align:vert center, horiz center_across_selection;')
        title_style = xlwt.easyxf('font: bold on; align: vert center, horiz center;\
                                   borders: top_color black, bottom_color black, right_color black, left_color black,\
                                   left thin, right thin, top thin, bottom thin')
        data_style = xlwt.easyxf('borders: top_color gray40, bottom_color gray40, right_color gray40, left_color gray40,\
                                   left thin, right thin, top thin, bottom thin')
        data_value_style = xlwt.easyxf('align: horiz right;\
                                   borders: top_color gray40, bottom_color gray40, right_color gray40, left_color gray40,\
                                   left thin, right thin, top thin, bottom thin')
        ab_value_style = xlwt.easyxf('align: horiz center;\
                                   borders: top_color gray40, bottom_color gray40, right_color gray40, left_color gray40,\
                                   left thin, right thin, top thin, bottom thin')
        total_style = xlwt.easyxf('align: horiz right; font: bold on;')
        total_value_style = xlwt.easyxf('align: horiz right')
        total_ab_style = xlwt.easyxf('align: horiz center')

        sheet = wbk.add_sheet('Customer Payment Details')

        # header
        if len(data) == 0:
            raise osv.except_osv(_('User Error!'), _('Belirtilen tarihler arasinda bir kayit bulunanamistir.'))

        sheet.write(0, 0, u"Cari: %s" % record.partner_id.name, style=header_style)
        if record.partner_id.x_vergidairesi:
            sheet.write(0, 6, u"Vergi Dairesi: %s" % record.partner_id.x_vergidairesi, style=header_style)
        if record.partner_id.vat:
            sheet.write(0, 8, u"Vergi No: %s" % record.partner_id.vat, style=header_style)
        sheet.write(0, 11, "Tarih: %s" % datetime.now().strftime("%d.%m.%Y"), style=header_style)

        # title

        sheet.write(1, 0, "No", style=title_style)
        sheet.write(1, 1, u"Sayı", style=title_style)
        sheet.write(1, 2, "Tarih", style=title_style)
        sheet.write(1, 3, "Vadesi", style=title_style)
        sheet.write(1, 4, u"Açıklama", style=title_style)
        sheet.write(1, 5, u"%s Borç" % second_currency.name, style=title_style)
        sheet.write(1, 6, "%s Alacak" % second_currency.name, style=title_style)
        sheet.write(1, 7, "%s Bakiye" % second_currency.name, style=title_style)
        sheet.write(1, 8, "B/A", style=title_style)
        sheet.write(1, 9, u"TL Borç", style=title_style)
        sheet.write(1, 10, "TL Alacak", style=title_style)
        sheet.write(1, 11, "TL Bakiye", style=title_style)
        sheet.write(1, 12, "B/A", style=title_style)

        row = 2
        for res in data:
            sheet.write(row, 0, row, style=data_style)
            sheet.write(row, 1, res['number'], style=data_style)
            sheet.write(row, 2, res['date'] or '', style=data_style)
            sheet.write(row, 3, res['due_date'] or '', style=data_style)
            sheet.write(row, 4, res['description'], style=data_style)
            sheet.write(row, 5, "%s%.2f" % (second_currency.symbol, res['sec_curr_debit']), style=data_value_style)
            sheet.write(row, 6, "%s%.2f" % (second_currency.symbol, res['sec_curr_credit']), style=data_value_style)
            sheet.write(row, 7, "%s%.2f" % (second_currency.symbol, res['sec_curr_balance']), style=data_value_style)
            sheet.write(row, 8, res['sec_curr_dc'], style=ab_value_style)
            sheet.write(row, 9, "%s%.2f" % (u"\u20BA", res['debit']), style=data_value_style)
            sheet.write(row, 10, "%s%.2f" % (u"\u20BA", res['credit']), style=data_value_style)
            sheet.write(row, 11, "%s%.2f" % (u"\u20BA", res['balance']), style=data_value_style)
            sheet.write(row, 12, res['dc'], style=ab_value_style)
            row += 1

        # footer and total row
        sheet.write(row, 6, "Toplam:", style=total_style)
        sheet.write(row, 7, "%s%.2f" % (second_currency.symbol, data[-1]['sec_curr_total']), style=total_value_style)
        sheet.write(row, 8, data[-1]['sec_curr_dc'], style=total_ab_style)

        sheet.write(row, 10, "Toplam:", style=total_style)
        sheet.write(row, 11, "%s%.2f" % (u"\u20BA", data[-1]['total']), style=total_value_style)
        sheet.write(row, 12, data[-1]['dc'], style=total_ab_style)

        # styling
        sheet.col(0).width = 1500
        sheet.col(1).width = 5000
        sheet.col(4).width = 5000
        sheet.col(5).width = 4000
        sheet.col(6).width = 4000
        sheet.col(7).width = 4000
        sheet.col(8).width = 1000
        sheet.col(9).width = 4000
        sheet.col(10).width = 4000
        sheet.col(11).width = 4000
        sheet.col(12).width = 1000

        sheet.row(0).height = 500
        sheet.row(1).height = 300

        wbk.save(fl)
        fl.seek(0)
        xlsx_file = base64.encodestring(fl.read())
        return xlsx_file

wizard_partner_doviz_statement()


class customer_statement_excel(osv.osv_memory):
   _name = "customer.statement.excel"

   def default_get(self, cr, uid, fields, context=None):
       if context is None:
           context = {}
       res = super(customer_statement_excel, self).default_get(cr, uid, fields, context=context)
       if context.get('file'):
           res.update({'file': context['file'], 'name':'Musteri_Dovizli_Ekstre.xls'})
       return res

   _columns = {
       'file': fields.binary('File'),
       'name': fields.char(string='File Name', size=64),
   }

customer_statement_excel()
