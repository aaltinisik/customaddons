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
import time
from StringIO import StringIO
import xlwt
import base64


class wizard_partner_detail(osv.osv_memory):
    _name = "wizard.partner.detail"
    _columns = {
        'start_date': fields.date('Start Date', required=True),
        'end_date': fields.date('End Date', required=True),
    }
    _defaults ={
         'start_date': lambda *a: time.strftime('%Y-01-01'),
         'end_date': lambda *a: time.strftime('%Y-%m-%d'),
    }

    def print_report(self, cr, uid, ids, context=None):
        record = self.browse(cr, uid, ids[0], context=context)
        partner_obj = self.pool.get('res.partner')
        query = self.pool.get('account.move.line')._query_get(cr, uid, context=context)
        if context and context.get('active_ids'):
            partner_ids = tuple(context['active_ids'])
        else:
            partner_ids = tuple(self.pool.get('res.partner').search(cr, uid, [], context=context))
        cr.execute("""SELECT l.partner_id, a.type, SUM(l.debit-l.credit)
                      FROM account_move_line l
                      LEFT JOIN account_account a ON (l.account_id=a.id)
                      WHERE a.type IN ('receivable','payable')
                      AND l.partner_id IN %s
                      AND l.date >= %s
                      AND l.date <= %s
                      GROUP BY l.partner_id, a.type""", (partner_ids, record.start_date, record.end_date))
        result = {}
        for id in partner_ids:
            result[id] = {'receivable': 0, 'payable': 0}
        for pid,type,val in cr.fetchall():
            for v in result:
                if v == pid:
                    result[pid][type] = (type=='receivable') and val or -val
        fl = StringIO()
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('Customer Payment Details')
        sheet.write(0, 0, "Customer Name")
        sheet.write(0, 1, "Phone")
        sheet.write(0, 2, "Credit")
        sheet.write(0, 3, "Debit")
        sheet.write(0, 4, "Balance")
        sheet.write(0, 5, "Zirve Kodu")
        sheet.write(0, 6, "Hesap kodu")
        sheet.write(0, 7, "Faks")
        sheet.write(0, 8, "Vergi No")
        sheet.write(0, 9, "Vergi Daire")
        sheet.write(0, 10, "Adres1")
        sheet.write(0, 11, "Adres2")
        sheet.write(0, 12, "ilce")
        sheet.write(0, 13, "il")
        sheet.write(0, 14, "ulke")
        row = 1
        for res in result.items():
            partner = partner_obj.browse(cr, uid, res[0])
            if not partner.is_company:
                continue
            sheet.write(row, 0, partner.name)
            sheet.write(row, 1, partner.phone or '')
            sheet.write(row, 2, res[1]['payable'])
            sheet.write(row, 3, res[1]['receivable'])
            sheet.write(row, 4, res[1]['receivable'] - res[1]['payable'])
#             sheet.write(row, 5, partner.z_muhasebe_kodu or '')
            sheet.write(row, 6, partner.ref or '')
            sheet.write(row, 7, partner.fax or '')
#             sheet.write(row, 8, partner.vat or '')
#             sheet.write(row, 9, partner.x_vergidairesi or '')
            sheet.write(row, 10, partner.street or '')
            sheet.write(row, 11, partner.street2 or '')
            sheet.write(row, 12, partner.city or '')
            sheet.write(row, 13, partner.state_id.name or '')
            sheet.write(row, 14, partner.country_id.name or '')
            row +=1
        wbk.save(fl)
        fl.seek(0)
        buffer = base64.encodestring(fl.read())
        ctx = dict(context)
        ctx.update({'file': buffer})
        form_id = self.pool.get('ir.model.data').get_object_reference(cr, uid,
                                                    'partner_payment_detail', 'customer_excel_form')[1]
        return {
           'type': 'ir.actions.act_window',
           'view_type': 'form',
           'view_mode': 'form',
           'res_model': 'customer.excel',
           'views': [(form_id, 'form')],
           'view_id': form_id,
           'target': 'new',
           'context': ctx,
        }

wizard_partner_detail()


class customer_excel(osv.osv_memory):
   _name = "customer.excel"

   def default_get(self, cr, uid, fields, context=None):
       if context is None:
           context = {}
       res = super(customer_excel, self).default_get(cr, uid, fields, context=context)
       if context.get('file'):
           res.update({'file': context['file'], 'name':'Customer_Detail.xls'})
       return res

   _columns = {
       'file': fields.binary('File'),
       'name': fields.char(string='File Name', size=64),
   }
customer_excel()
