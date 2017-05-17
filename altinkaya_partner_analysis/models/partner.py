# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from openerp import models, fields, api, _

class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def open_partner_invoice_analysis(self):
        invoice_analysis_view_ref = self.env['ir.model.data'].get_object_reference('account', 'view_account_invoice_report_graph')
        view_id = invoice_analysis_view_ref and invoice_analysis_view_ref[1] or False,
        context = {}
        context.update({'search_default_current':1,
                        'search_default_thisyear':1,
                        'group_by':'period_id',
                        'search_default_partner_id':self.id})
        if self._context and self._context.get('customer'):
            context.update({'search_default_customer':1})
            return {
                    'type': 'ir.actions.act_window',
                    'name': _(u'Invoices Analysis'),
                    'res_model': 'account.invoice.report',
                    'view_type': 'graph',
                    'view_mode': 'graph',
                    'view_id': view_id,
                    'target': 'current',
                    'nodestroy': True,
                    'context':context
                }
        if self._context and self._context.get('supplier'):
            context.update({'search_default_supplier':1})
            return {
                    'type': 'ir.actions.act_window',
                    'name': _(u'Invoices Analysis'),
                    'res_model': 'account.invoice.report',
                    'view_type': 'graph',
                    'view_mode': 'graph',
                    'view_id': view_id,
                    'target': 'current',
                    'nodestroy': True,
                    'context':context
                }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: