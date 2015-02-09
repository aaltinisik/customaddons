# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2013-Present Acespritech Solutions Pvt. Ltd. (<http://acespritech.com>).
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

from openerp.osv import fields
from openerp.osv import osv
from openerp.tools.translate import _
import netsvc
import base64

class res_partner(osv.osv):
    _inherit = 'res.partner'

    def send_statement_fax(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        attach_obj = self.pool.get('ir.attachment')
        sendfax_obj = self.pool.get('faxsend.queue')
        faxacc_id = self.pool.get('faxsend.account').search(cr, uid, [])
        if not faxacc_id:
            return True
        service = netsvc.LocalService('report.partner.statement2')
        for partner in self.browse(cr, uid, ids):
            faxno = partner.fax
            if not faxno:
                faxno = partner.parent_id.fax
                if not faxno:
                    raise osv.except_osv(_('Error'),
                                         _('Customer has no faxno'))

            report_datas = {
                'ids': [partner.id],
                'model': 'res.partner',
            }
            (report_file, format) = service.create(cr, uid, [partner.id], report_datas, context)
            if not report_file:
                continue
            attachment_id = attach_obj.create(cr, uid, {'name': partner.name,
                                                        'res_model': 'res.partner',
                                                        'res_id': partner.id,
                                                        'res_name': partner.name,
                                                        'partner_id': partner.id,
                                                        'datas': base64.b64encode(report_file),
                                                        'datas_fname': partner.ref+'_fax.pdf',
                                                        })
            fax_val = {
                'report': 'res.partner',
                'faxno': faxno,
                'object_type': 'attachment',
                'obj_id': partner.id,
                'subject': partner.name,
                'account_id': faxacc_id[0],
                'state': 'wait',
                'retry_counter':0,
                'attachment_id': attachment_id,
            }
            fax_id = sendfax_obj.create(cr, uid, fax_val)
            sendfax_obj.process_faxes(cr, uid, [fax_id], context=context)
            message = "Cari Ekstre Faks Gönderildi."
            self.message_post(cr, uid, [partner.id], body=message, context=context)

        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: