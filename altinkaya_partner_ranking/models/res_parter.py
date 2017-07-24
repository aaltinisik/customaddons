# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = 'res.partner'
    _order = 'ranking'

    ranking = fields.Integer('Ranking')

    @api.model
    def evaluate_ranking(self):
        """
        scheduler for partner ranking.
        """
        context = self._context
        if context is None:
            context = {}
        _logger.info("\nScheduler started:: For partner ranking......................")
        invoice_obj = self.env['account.invoice']
        
        today_date = datetime.now().date()
        prev_year = (today_date.year) - 1
        prev_year_date = str(prev_year) + "-01-01"
        self._cr.execute('''SELECT partner_id, COALESCE(sum(amount_total), 0) FROM account_invoice
                            WHERE state not in ('draft', 'cancel', 'proforma', 'proforma2')
                            AND type = 'out_invoice'
                            AND date_invoice >= '%s'
                            GROUP BY partner_id
                        ''' %(prev_year_date))
        out_inv_datas = self._cr.fetchall()
        res_out_inv_dict = dict(out_inv_datas)
        self._cr.execute('''SELECT partner_id, COALESCE(sum(amount_total), 0) FROM account_invoice
                            WHERE state not in ('draft', 'cancel', 'proforma', 'proforma2')
                            AND type = 'out_refund'
                            AND date_invoice >= '%s'
                            GROUP BY partner_id
                        ''' %(prev_year_date))
        out_refund_datas = self._cr.fetchall()
        res_out_refund_dict = dict(out_refund_datas)
        result_dict = res_out_inv_dict
        for k,v in res_out_refund_dict.iteritems():
            if k in result_dict.keys():
                result_dict.update({k: result_dict.get(k) - v})
        result_dict = dict((y,x) for x,y in result_dict.iteritems())
        partner_inv_data = []
        if result_dict:
            res_dict = dict(result_dict)
            partner_inv_data = sorted(res_dict.iteritems(), key=lambda (k,v): (k,v),reverse=True)
        all_partner_lst = self.search([]).ids
        inv_partner_lst = []
        rank_number = 1
        for datas_inv_partner in partner_inv_data:
            partner_rec = self.browse(datas_inv_partner[1])
            partner_rec.ranking = rank_number
            rank_number += 1
            inv_partner_lst.append(datas_inv_partner[1])
        remain_partner_lst = list(set(all_partner_lst) - set(inv_partner_lst))
        if remain_partner_lst:
            self.browse(remain_partner_lst).write({'ranking': 999999})
        return True