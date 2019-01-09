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

from openerp.osv import fields, osv
from datetime import date
import time


class partner_statement_wizrd(osv.osv_memory):
    _name = 'partner.statement.wizard'

    def start_date(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        return date(date.today().year, 1, 1).strftime('%Y-%m-%d')

    def end_date(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        return date(date.today().year, 12, 31).strftime('%Y-%m-%d')

    _columns = {
        'date_start': fields.date('Start Date', required=1),
        'date_end': fields.date('End Date', required=1),
    }
    _defaults = {
        'date_start': start_date,
        'date_end': end_date,
    }

    def print_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = {
            'ids': context.get('active_ids',[]),
            'model': 'res.partner',
            'form': self.read(cr, uid, ids)[0]
        }
        return {
            'type' : 'ir.actions.report.xml',
            'report_name':'partner.statement',
            'datas': data,
       }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
