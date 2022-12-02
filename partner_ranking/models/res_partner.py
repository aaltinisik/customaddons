from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class PartnerRank(models.Model):
    _name = 'res.partner.rank'
    _description = "Partner Ranking"

    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    date_rank = fields.Date('Ranking Date', required=True)
    rank = fields.Integer('Rank', required=True)
    total = fields.Float('Total Revenue', required=True)


class Partner(models.Model):
    _inherit = 'res.partner'
    _order = 'ranking,name'

    ranking = fields.Integer('Ranking', default=999999)

    @api.model
    def evaluate_ranking(self):
        """
        scheduler for partner ranking.
        """
        context = self._context
        if context is None:
            context = {}
        _logger.info(
            "\nScheduler started:: For partner ranking......................")
        # invoice_obj = self.env['account.invoice']
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=720)
        self._cr.execute('''
                            INSERT INTO res_partner_rank(partner_id, date_rank, rank, total)
                            SELECT commercial_partner_id, '%s', 
                                CASE  WHEN total > 0 THEN row_number() OVER(ORDER BY total DESC) 
                                ELSE 999999 END
                            AS ranking,total FROM 
                            (

                                select p.commercial_partner_id, coalesce(pir.total,0.0) as total
                                from ( select distinct commercial_partner_id from res_partner) p 
                                left join 
                                    (select commercial_partner_id, SUM(price_total_usd) as total from  account_invoice_report 
                                WHERE 
                                    state not in ('draft', 'cancel','proforma','proforma2') AND
                                    type in('out_refund', 'out_invoice') AND
                                    price_total_usd > 20 AND
                                    date >= '%s' 
                                    GROUP BY commercial_partner_id) pir
                                on p.commercial_partner_id = pir.commercial_partner_id

                            ) as Rank
                        ''' % (
        start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))

        self._cr.execute('''
                            UPDATE res_partner p set ranking = r.rank
                            from (SELECT * FROM res_partner_rank ORDER BY date_rank DESC) r 
                            WHERE p.commercial_partner_id = r.partner_id 
                        ''')

#         out_inv_datas = self._cr.fetchall()
#         all_partners = self.env['res.partner'].search([]).ids
#         invoice_partner_list = []
# 
#         remain_partner_lst = []
#         for info in out_inv_datas:
#             partner_id = info[0]
#             partner = self.env['res.partner'].search([('id', '=', partner_id)])
#             partner.write({'ranking': info[1]})
#             
#             invoice_partner_list.append(info[0])
#         
#         remain_partner_lst = list(set(all_partners) - set(invoice_partner_list))
#         if remain_partner_lst:
#             self.browse(remain_partner_lst).write({'ranking': 999999})
# 
#         for info in self.env['res.partner'].search([]).ids:
#             partner_id = info
#             partner = self.env['res.partner'].search([('id', '=', partner_id)])
#             if partner.commercial_partner_id:
#                 partner.write({'ranking': partner.commercial_partner_id.ranking})
