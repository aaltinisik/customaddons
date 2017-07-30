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
        self._cr.execute('''
                            SELECT commercial_partner_id, row_number() OVER(ORDER BY total DESC)
                            AS ranking,total FROM 
                            (SELECT commercial_partner_id, SUM(price_total) as total FROM
                            account_invoice_report WHERE 
                            state not in ('draft', 'cancel','proforma','proforma2') AND
                            type in('out_refund', 'out_invoice') AND
                            date >= '%s'
                            GROUP BY commercial_partner_id) as Rank ORDER BY total DESC
                        ''' %(prev_year_date))

        out_inv_datas = self._cr.fetchall()
        all_partners = self.env['res.partner'].search([]).ids
        invoice_partner_list = []
        remain_partner_lst = []
        for info in out_inv_datas:
            partner_id = info[0]
            partner = self.env['res.partner'].search([('id', '=', partner_id)])
            partner.write({'ranking': info[1]})
            invoice_partner_list.append(info[0])


        remain_partner_lst = list(set(all_partners) - set(invoice_partner_list))
        if remain_partner_lst:
            self.browse(remain_partner_lst).write({'ranking': 999999})
        return True