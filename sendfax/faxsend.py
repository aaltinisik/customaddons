# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 solutions2use (<http://www.solutions2use.com>).
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

from osv import osv, fields
from tools.translate import _
import openerp.netsvc as netsvc
from interfax import client
import time, datetime
import logging
import base64
import re
import os.path

logger = logging.getLogger('faxsend')


class faxsend_account(osv.osv):
    _name = 'faxsend.account'
    _columns = {
        'name': fields.char('Account', size=50, required=True),
        'username': fields.char('Username', size=50, required=True),
        'password': fields.char('Password', size=50, required=True),
    }
    _sql_constraints = [
        ('pu-key', 'UNIQUE (name)', 'Account already exists in database!'),
    ]


class faxsend_queue(osv.osv):

    def _get_name(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for r in self.browse(cr, uid, ids):
            res[r.id] = r.report + '/' + r.subject + '/' + str(r.obj_id)
        return res

    def _process_faxes(self, cr, uid, ids=False, context=None):
        if not ids:
            ids = self.search(cr, uid, [('state', '=', 'wait')])
        return self.process_faxes(cr, uid, ids, context=context)

    _name = 'faxsend.queue'
    _order = 'queue_date desc, id desc'
    _columns = {
       'name': fields.function(_get_name, method=True, type='char', size=50, string='Queue'),
       'report': fields.char('Report/Model', size=50, required=True, readonly=True, states={'draft': [('readonly', False)]}),
       'object_type': fields.selection([
            ('report', 'Report'),
            ('attachment', 'Attachment'),
            ], 'Obj type', required=True, select=True, readonly=True, states={'draft': [('readonly', False)]}),
       'obj_id': fields.integer('Obj. ID', required=True, readonly=True, states={'draft': [('readonly', False)]}),
       'state': fields.selection([
            ('draft', 'Draft'),
            ('wait', 'Waiting'),
            ('send', 'Sending'),
            ('error', 'Error'),
            ('ok', 'Send ok'),
            ('cancel', 'Cancelled'),
            ], 'Fax State', readonly=True, help="Gives the state of the fax.", select=True),
       'faxno': fields.char('Fax No.', size=50, required=True, readonly=True, states={'draft': [('readonly', False)]}),
       'job_no': fields.char('Job', size=50, select=True, readonly=True, states={'draft': [('readonly', False)]}),
       'pages': fields.integer('Pages', readonly=True),
       'duration': fields.integer('Duration (sec.)', readonly=True),
       'subject': fields.char('Subject', size=50, required=True, readonly=True, states={'draft': [('readonly', False)]}),
       'account_id': fields.many2one('faxsend.account', 'Account', select=True, required=True, readonly=True, states={'draft': [('readonly', False)]}),
       'queue_date': fields.date('Date of entry'),
       'trigger_model': fields.char('Trigger model', size=50, readonly=True, states={'draft': [('readonly', False)]}),
       'trigger_method': fields.char('Trigger method', size=50, readonly=True, states={'draft': [('readonly', False)]}),
       'trigger_method_args': fields.char('Method args', size=50, readonly=True, states={'draft': [('readonly', False)]}),
       'retry_counter': fields.integer('Retry'),
    }
    _defaults = {
        'object_type': 'report',
        'state': 'draft',
        'queue_date': lambda *a: time.strftime('%Y-%m-%d'),
        'trigger_method_args': '()',
        'retry_counter': 0,
    }

    def send_report_by_fax(self, cr, uid, obj_id, account, subject, report, faxno,
                           triggerModel=None, triggerMethod=None, triggerArgs=None):
        acc_id = self.pool.get('faxsend.account').search(cr, uid,
                                                    [('name', '=', account)])
        if not acc_id:
            raise osv.except_osv(_('Error :'),
                                 _('Account \'%s\' for send fax not found.') % account)
        self.create(cr, uid, {'report': report,
                               'obj_id': obj_id,
                               'faxno': faxno,
                               'subject': subject,
                               'account_id': acc_id[0],
                               'object_type': 'report',
                               'trigger_model': triggerModel,
                               'trigger_method': triggerMethod,
                               'trigger_method_args': triggerArgs,
                               'state': 'wait'})
        return True

    def send_attachment_by_fax(self, cr, uid, obj_id, account, subject, model,
                               faxno, triggerModel=None, triggerMethod=None, triggerArgs=None):
        acc_id = self.pool.get('faxsend.account').search(cr, uid,
                                                [('name', '=', account)])
        if not acc_id:
            raise osv.except_osv(_('Error :'),
                                 _('Account \'%s\' for send fax not found.') % account)
        self.create(cr, uid, {'report': model,
                               'obj_id': obj_id,
                               'faxno': faxno,
                               'subject': subject,
                               'account_id': acc_id[0],
                               'object_type': 'attachment',
                               'trigger_model': triggerModel,
                               'trigger_method': triggerMethod,
                               'trigger_method_args': triggerArgs,
                               'state': 'wait'})
        return True

    def action_send_fax(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'wait'})
        return True

    def action_send_fax_again(self, cr, uid, ids, *args):
        if not ids:
            return False
        # set state='draft' gives user chance to change data before sending fax
        self.write(cr, uid, ids, {'state': 'draft', 'job_no':'' })
        wf_service = netsvc.LocalService("workflow")
        for id in ids:
            # Deleting the existing instance of workflow for faxsend.queue
            wf_service.trg_delete(uid, 'faxsend.queue', id, cr)
            wf_service.trg_create(uid, 'faxsend.queue', id, cr)
        return True

    def action_cancel_send_fax(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'cancel'})
        return True

    def process_faxes(self, cr, uid, ids, context=None):
        """WARNING: meant for cron usage only - will commit() after each fax!"""
        # first let us check the status of faxes previous send by the scheduler
        msg_obj = self.pool.get('mail.message')
        user_obj = self.pool.get("res.users")
        list = self.search(cr, uid, [('state', '=', 'send')], order='job_no desc', context=context)
        if list:
            try:
                o = self.browse(cr, uid, list[0])
                c = client.InterFaxClient(o.account_id.username, o.account_id.password)
                (result, faxItems) = c.faxStatus(int(o.job_no) + 1, len(list))
                if result == 0:
                    for i in faxItems:
                        # i[0] = TransactionID
                        # i[6] = Pages
                        # i[7] = Status
                        # i[8] = Duration
                        if i[7] >= 0:
                            list = self.search(cr, uid, [('state', '=', 'send'),
                                                         ('job_no', '=', i[0])], context=context)
                            if list:
                                o = self.browse(cr, uid, list[0])
                                if o.trigger_model and o.trigger_method:
                                    faxResult = 'ok' if i[7] == 0 else 'error'
                                    try:
                                        obj = self.pool.get(o.trigger_model)
                                        func = getattr(obj, o.trigger_method)
                                    except AttributeError:
                                        logger.error('Trigger failed. Model %s and/or method %s do not exists.' % (o.trigger_model, o.trigger_method))
                                    else:
                                        result = func(cr, uid, faxResult, sendPages=i[6],
                                                      sendDuration=i[8], args=eval(o.trigger_method_args))
                                if i[7] == 0:
                                    self.write(cr, uid, list, {'state': 'ok', 'pages': i[6],
                                                               'duration': i[8]})
                                else:
                                    if o.retry_counter < 5:
                                        self.write(cr, uid, [o.id], {'retry_counter': o.retry_counter + 1,
                                                                     'state': 'wait'})
                                    else:
                                        cr.execute('select create_uid from faxsend_queue where id=%s', (o.id,))
                                        data = cr.fetchone()
                                        create_uid = data and data[0] or False
                                        notified_partner_id = user_obj.browse(cr, uid, create_uid).partner_id.id
                                        body = "This fax failed to send: <b><a href='#id=%s&view_type=form&model=faxsend.queue'>%s</a></b>" % (str(o.id), o.faxno)
                                        msg_obj.create(cr, uid, {
                                            'notified_partner_ids': [(6, 0, [notified_partner_id])],
                                            'body': body,
                                            'subject': 'Regarding Fax Fail',
                                            'type': 'notification',
                                        })
                                        self.write(cr, uid, list, {'state': 'error'})
                                cr.commit()
            except Exception:
                logger.error('failed retrieving fax-status from interfax.net')

        # now let us fax the new ones
        for id in ids:
            # send fax
            # depending on result set state to 'send' or to 'error'
            o = self.browse(cr, uid, id)
            if o.object_type == 'report':
                try:
                    ir_actions_report = self.pool.get('ir.actions.report.xml')
                    matching_reports = ir_actions_report.search(cr, uid, [('report_name', '=', o.report)])
                    if matching_reports:
                        report = ir_actions_report.browse(cr, uid, matching_reports[0])
                        service = netsvc.LocalService('report.%s' % (report.report_name))
                        (faxData, format) = service.create(cr, uid, [o.obj_id], {}, {})
                        c = client.InterFaxClient(o.account_id.username, o.account_id.password)
                        result = c.sendFaxStream(o.faxno, faxData, report.report_type)

                        if (result > 0):
                            ir_attachment_pool = self.pool.get('ir.attachment')
                            faxData = base64.b64encode(faxData)
                            file_name = o.subject
                            file_name = re.sub(r'[^a-zA-Z0-9_-]', '_', file_name)
                            file_name += '.%s' % (report.report_type)
                            ir_attachment = ir_attachment_pool.create(cr, uid, {'name': file_name,
                                                                                'datas': faxData,
                                                                                'datas_fname': file_name,
                                                                                'res_model': 'faxsend.queue',
                                                                                'res_id': o.id},
                                                                                context=context)
                            self.write(cr, uid, [o.id], {'state': 'send',
                                                         'job_no': result})
                        else:
                            if o.retry_counter < 5:
                                self.write(cr, uid, [o.id], {'retry_counter': o.retry_counter + 1,
                                                             'state': 'wait'})
                            else:
                                cr.execute('select create_uid from faxsend_queue where id=%s', (o.id,))
                                data = cr.fetchone()
                                create_uid = data and data[0] or False
                                notified_partner_id = user_obj.browse(cr, uid, create_uid).partner_id.id
                                body = "This fax failed to send: <b><a href='#id=%s&view_type=form&model=faxsend.queue'>%s</a></b>" % (str(o.id), o.faxno)
                                msg_obj.create(cr, uid, {
                                    'notified_partner_ids': [(6, 0, [notified_partner_id])],
                                    'body': body,
                                    'subject': 'Regarding Fax Fail',
                                    'type': 'notification',
                                })
                                self.write(cr, uid, [o.id], {'state': 'error',
                                                             'job_no': str(result)})
                    else:
                        if o.retry_counter < 5:
                            self.write(cr, uid, [o.id], {'retry_counter': o.retry_counter + 1,
                                                         'state': 'wait'})
                        else:
                            cr.execute('select create_uid from faxsend_queue where id=%s', (o.id,))
                            data = cr.fetchone()
                            create_uid = data and data[0] or False
                            notified_partner_id = user_obj.browse(cr, uid, create_uid).partner_id.id
                            body = "This fax failed to send: <b><a href='#id=%s&view_type=form&model=faxsend.queue'>%s</a></b>" % (str(o.id), o.faxno)
                            msg_obj.create(cr, uid, {
                                'notified_partner_ids': [(6, 0, [notified_partner_id])],
                                'body': body,
                                'subject': 'Regarding Fax Fail',
                                'type': 'notification',
                            })
                            self.write(cr, uid, [o.id], {'state': 'error',
                                                         'job_no': 'Report %s not found' % (o.report) })
                except Exception:
                    logger.error('failed sending fax %s', o.name)
                    if o.retry_counter < 5:
                        self.write(cr, uid, [o.id], {'retry_counter': o.retry_counter + 1,
                                                     'state': 'wait'})
                    else:
                        cr.execute('select create_uid from faxsend_queue where id=%s', (o.id,))
                        data = cr.fetchone()
                        create_uid = data and data[0] or False
                        notified_partner_id = user_obj.browse(cr, uid, create_uid).partner_id.id
                        body = "This fax failed to send: <b><a href='#id=%s&view_type=form&model=faxsend.queue'>%s</a></b>" % (str(o.id), o.faxno)
                        msg_obj.create(cr, uid, {
                            'notified_partner_ids': [(6, 0, [notified_partner_id])],
                            'body': body,
                            'subject': 'Regarding Fax Fail',
                            'type': 'notification',
                        })
                        self.write(cr, uid, [o.id], {'state': 'error'})
            elif o.object_type == 'attachment':
                try:
                    ir_attachment = self.pool.get('ir.attachment')
                    attachment_ids = ir_attachment.search(cr, uid, [('res_model', '=', o.report),
                                                                    ('res_id', '=', o.obj_id)])
                    if attachment_ids:
                        attachment = ir_attachment.browse(cr, uid, attachment_ids[0], context=context)
                        faxData = base64.b64decode(attachment.datas)
                        docType = os.path.splitext(attachment.datas_fname)[1][1:]
                        if not docType:
                            docType = "pdf"

                        c = client.InterFaxClient(o.account_id.username, o.account_id.password)
                        result = c.sendFaxStream(o.faxno, faxData, docType)

                        if (result > 0):
                            self.write(cr, uid, [o.id], {'state': 'send', 'job_no': result})
                        else:
                            if o.retry_counter < 5:
                                self.write(cr, uid, [o.id], {'retry_counter': o.retry_counter + 1,
                                                             'state': 'wait'})
                            else:
                                cr.execute('select create_uid from faxsend_queue where id=%s', (o.id,))
                                data = cr.fetchone()
                                create_uid = data and data[0] or False
                                notified_partner_id = user_obj.browse(cr, uid, create_uid).partner_id.id
                                body = "This fax failed to send: <b><a href='#id=%s&view_type=form&model=faxsend.queue'>%s</a></b>" % (str(o.id), o.faxno)
                                msg_obj.create(cr, uid, {
                                    'notified_partner_ids': [(6, 0, [notified_partner_id])],
                                    'body': body,
                                    'subject': 'Regarding Fax Fail',
                                    'type': 'notification',
                                })
                                self.write(cr, uid, [o.id], {'state': 'error',
                                                             'job_no': str(result)})
                    else:
                        if o.retry_counter < 5:
                            self.write(cr, uid, [o.id], {'retry_counter': o.retry_counter + 1,
                                                         'state': 'wait'})
                        else:
                            cr.execute('select create_uid from faxsend_queue where id=%s', (o.id,))
                            data = cr.fetchone()
                            create_uid = data and data[0] or False
                            notified_partner_id = user_obj.browse(cr, uid, create_uid).partner_id.id
                            body = "This fax failed to send: <b><a href='#id=%s&view_type=form&model=faxsend.queue'>%s</a></b>" % (str(o.id), o.faxno)
                            msg_obj.create(cr, uid, {
                                'notified_partner_ids': [(6, 0, [notified_partner_id])],
                                'body': body,
                                'subject': 'Regarding Fax Fail',
                                'type': 'notification',
                            })
                            self.write(cr, uid, [o.id], {'state': 'error',
                                                         'job_no': 'Attachment %s not found' % (o.report)})
                except Exception:
                    logger.error('failed sending fax %s', o.name)
                    if o.retry_counter < 5:
                        self.write(cr, uid, [o.id], {'retry_counter': o.retry_counter + 1,
                                                     'state': 'wait'})
                    else:
                        cr.execute('select create_uid from faxsend_queue where id=%s', (o.id,))
                        data = cr.fetchone()
                        create_uid = data and data[0] or False
                        notified_partner_id = user_obj.browse(cr, uid, create_uid).partner_id.id
                        body = "This fax failed to send: <b><a href='#id=%s&view_type=form&model=faxsend.queue'>%s</a></b>" % (str(o.id), o.faxno)
                        msg_obj.create(cr, uid, {
                            'notified_partner_ids': [(6, 0, [notified_partner_id])],
                            'body': body,
                            'subject': 'Regarding Fax Fail',
                            'type': 'notification',
                        })
                        self.write(cr, uid, [o.id], {'state': 'error'})
            # we must do this because scheduler is calling this method
            # if an error occured we dont want the faxes send succesfully rolled back            
            cr.commit()
