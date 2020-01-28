# -*- coding: utf-8 -*- 
'''
Created on Jan 28, 2018

@author: Codequarters
'''
from odoo import models, fields, api


class Currency(models.Model):
    _inherit = "res.currency"

    @api.multi
    def _compute_current_rate(self):
        date = self._context.get('date') or fields.Date.today()
        company = self.env['res.users']._get_company()
        company_id = company.id
        currency_rate_type_id = company.currency_rate_type_id and company.currency_rate_type_id.id or 1
        # the subquery selects the last rate before 'date' for the given currency/company
        query = """SELECT c.id, (SELECT r.rate FROM res_currency_rate r
                                  WHERE r.currency_id = c.id AND r.name <= %s
                                    AND (r.company_id IS NULL OR r.company_id = %s)
                                    AND (r.currency_rate_type_id IS NULL OR r.currency_rate_type_id = %s)
                               ORDER BY r.company_id, r.name DESC
                                  LIMIT 1) AS rate
                   FROM res_currency c
                   WHERE c.id IN %s"""
        self._cr.execute(query, (date, company_id, currency_rate_type_id, tuple(self.ids)))
        currency_rates = dict(self._cr.fetchall())
        for currency in self:
            currency.rate = currency_rates.get(currency.id) or 1.0
