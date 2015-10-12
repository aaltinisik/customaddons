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


class res_partner(osv.osv):
    _inherit = 'res.partner'

    def email_statement(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data_model = self.pool.get('ir.model.data')
        template_obj = self.pool.get('email.template')
        template = data_model.get_object(cr, uid, 'altinkaya_statement', 'email_template_edi_send_statement')
        mail_id = template_obj.send_mail(cr, uid, template.id, ids[0], force_send=True, context=context)
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
