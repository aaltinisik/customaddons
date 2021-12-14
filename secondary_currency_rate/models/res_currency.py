from odoo import models, fields, api
import logging


_logger = logging.getLogger(__name__)


class ResCurrencySecond(models.Model):
    _inherit = 'res.currency'

    second_rate = fields.Float(compute='_compute_second_rate', string='Second Rate', digits=(12, 6),
                        help='The rate of the currency to the currency of rate 1.')

    @api.multi
    @api.depends('rate_ids.second_rate')
    def _compute_second_rate(self):
        date = self._context.get('date') or fields.Date.today()
        company = self.env['res.company'].browse(self._context.get('company_id')) or self.env['res.users']._get_company()
        currency_rates = self._get_second_rates(company, date)
        for currency in self:
            currency.second_rate = currency_rates.get(currency.id) or 1.0

    def _get_second_rates(self, company, date):
        query = """SELECT c.id,
                          COALESCE((SELECT r.second_rate FROM res_currency_rate r
                                  WHERE r.currency_id = c.id AND r.name <= %s
                                    AND (r.company_id IS NULL OR r.company_id = %s)
                               ORDER BY r.company_id, r.name DESC
                                  LIMIT 1), 1.0) AS rate
                   FROM res_currency c
                   WHERE c.id IN %s"""
        self._cr.execute(query, (date, company.id, tuple(self.ids)))
        currency_rates = dict(self._cr.fetchall())
        return currency_rates
