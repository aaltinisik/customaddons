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


class followup_line(osv.osv):
    _inherit = 'account_followup.followup.line'
    _columns = {
        'send_fax': fields.boolean('Send a Fax', help="When processing, it will send a fax"),
    }


class account_followup_print(osv.osv_memory):
    _inherit = 'account_followup.print'

    def process_partners(self, cr, uid, partner_ids, data, context=None):
        partner_obj = self.pool.get('res.partner')
        msg_obj = self.pool.get('mail.message')
        sendfax_obj = self.pool.get('faxsend.queue')
        faxacc_obj = self.pool.get('faxsend.account')
        partner_ids_to_print = []
        nbmanuals = 0
        manuals = {}
        nbmails = 0
        nbfax = 0
        nbunknownmails = 0
        nbprints = 0
        resulttext = " "
        for partner in self.pool.get('account_followup.stat.by.partner').browse(cr, uid, partner_ids, context=context):
            if partner.amount_overdue < 10.0:
                continue
            if partner.max_followup_id.manual_action:
                partner_obj.do_partner_manual_action(cr, uid, [partner.partner_id.id], context=context)
                nbmanuals = nbmanuals + 1
                key = partner.partner_id.payment_responsible_id.name or _("Anybody")
                if not key in manuals.keys():
                    manuals[key] = 1
                else:
                    manuals[key] = manuals[key] + 1
            if partner.max_followup_id.send_email:
                nbunknownmails += partner_obj.do_partner_mail(cr, uid, [partner.partner_id.id], context=context)
                nbmails += 1
            if partner.max_followup_id.send_letter:
                partner_ids_to_print.append(partner.id)
                nbprints += 1
                message = "%s<I> %s </I>%s" % (_("Follow-up letter of "), partner.partner_id.latest_followup_level_id_without_lit.name, _(" will be sent"))
                partner_obj.message_post(cr, uid, [partner.partner_id.id], body=message, context=context)

            if partner.max_followup_id.send_fax:
                faxacc_id = faxacc_obj.search(cr, uid, [])
                if not faxacc_id:
                    continue
                if not partner.partner_id.fax:
                    message_body = _("Define faxno for sending fax for payment followup report.")
                    msg_obj.create(cr, uid, {
                        'res_id': partner.partner_id.id,
                        'notified_partner_ids': [(6, 0, [partner.partner_id.id])],
                        'body': message_body,
                        'model': 'res.partner',
                        'subject': 'Regarding Fax Fail',
                        'type': 'notification',
                    })
                    continue
                fax_val = {
                    'report': 'account_followup.followup.print',
                    'faxno': partner.partner_id.fax,
                    'object_type': 'report',
                    'obj_id': partner.partner_id.id,
                    'subject': 'followup',
                    'account_id': faxacc_id[0],
                    'state': 'wait',
                }
                fax_id = sendfax_obj.create(cr, uid, fax_val)
                sendfax_obj.process_faxes(cr, uid, [fax_id], context=context)
                nbfax += 1

        if nbunknownmails == 0:
            resulttext += str(nbmails) + _(" email(s) sent")
        else:
            resulttext += str(nbmails) + _(" email(s) should have been sent, but ") + str(nbunknownmails) + _(" had unknown email address(es)") + "\n <BR/> "
        resulttext += "<BR/>" + str(nbprints) + _(" letter(s) in report") + " \n <BR/>" + str(nbmanuals) + _(" manual action(s) assigned:")

        resulttext += "<BR/>" + str(nbfax) + _(" fax(s) sent") + " \n <BR/>"

        needprinting = False
        if nbprints > 0:
            needprinting = True
        resulttext += "<p align=\"center\">"
        for item in manuals:
            resulttext = resulttext + "<li>" + item + ":" + str(manuals[item]) + "\n </li>"
        resulttext += "</p>"
        result = {}
        action = partner_obj.do_partner_print(cr, uid, partner_ids_to_print, data, context=context)
        result['needprinting'] = needprinting
        result['resulttext'] = resulttext
        result['action'] = action or {}
        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
