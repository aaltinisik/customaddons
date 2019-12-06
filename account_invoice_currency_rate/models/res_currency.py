# -*- coding: utf-8 -*-

from odoo import models, api


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    @api.model
    def _get_currency_rate_for_date(self, currency, rate_date, currency_rate_type, company):
        rate = currency.rate_ids.search([
            ('currency_id','=', currency.id),
            ('name','ilike', rate_date),
            ('currency_rate_type_id','=', currency_rate_type.id),
            ('company_id','=', company.id)], limit=1)
        return 1.0 / (rate.rate or 1.0)

    @api.model
    def _get_conversion_rate(self, from_currency, to_currency,company,date):
        use_custom_rate = self._context.get('use_custom_rate')
        custom_rate = self._context.get('custom_rate')
        use_currency_rate = self._context.get('use_currency_rate')
        rate_type = self._context.get('currency_rate_type_id')
        rate_date = self._context.get('rate_date')
        company_id = self._context.get('company_id')
        if isinstance(company_id, int):
            company_id = self.env['res.company'].browse(company_id)
             
        if use_custom_rate and custom_rate:
            return custom_rate
        elif use_currency_rate and rate_type and rate_date and company_id:
            return self._get_currency_rate_for_date(company_id.currency_id, rate_date, rate_type, company_id)
        else:
            return super(ResCurrency, self)._get_conversion_rate(from_currency, to_currency,company=company,date=date)
