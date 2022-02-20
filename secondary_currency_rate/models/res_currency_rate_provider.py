# Copyright 2021 Yiğit Budak (https://github.com/yibudak)
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from sys import exc_info
from odoo.exceptions import UserError
import requests
from lxml.etree import fromstring
from datetime import datetime, timedelta, date


_logger = logging.getLogger(__name__)


class ResCurrencyRateProviderSecondRate(models.Model):
    _inherit = 'res.currency.rate.provider'

    second_service_rate_type = fields.Selection([
        ('ForexBuying', _('Forex Buy')),
        ('ForexSelling', _('Forex Sell')),
        ('BanknoteBuying', _('Banknote Buy')),
        ('BanknoteSelling', _('Banknote Sell'))
        ], string='Second Rate Type', default="BanknoteSelling")

    def rate_retrieve(self, dom, currency, rate_type, second_rate_type):
        res = {}
        xpath_currency_rate = "./Currency[@Kod='%s']/%s" % (currency.upper(), rate_type)
        xpath_second_currency_rate = "./Currency[@Kod='%s']/%s" % (currency.upper(), second_rate_type)

        res['rate_currency'] = [
            float(dom.findall(xpath_currency_rate)[0].text),
            float(dom.findall(xpath_second_currency_rate)[0].text),
        ]

        xpath_rate_ref = "./Currency[@Kod='%s']/Unit" % currency.upper()
        res['rate_ref'] = float(dom.findall(xpath_rate_ref)[0].text)
        return res

    def get_tcmb_currency_data(self, url, currencies):
        response = requests.get(url).text
        dom = fromstring(response.encode('utf-8'))

        _logger.debug("TCMB sent a valid XML file")

        currency_data = {}
        rate_type = self.service_rate_type
        second_rate_type = self.second_service_rate_type

        for currency in currencies:
            curr_data = self.rate_retrieve(dom, currency, rate_type, second_rate_type)
            rates = [curr_data['rate_ref'] / x or 1.0 for x in curr_data['rate_currency']]
            currency_data[currency] = rates

        return currency_data


    @api.multi
    def _update(self, date_from, date_to, newest_only=False):

        if self.service != 'TCMB':
            return super()._update(date_from, date_to, date_from, date_to, newest_only)

        Currency = self.env['res.currency']
        CurrencyRate = self.env['res.currency.rate']
        is_scheduled = self.env.context.get('scheduled')
        for provider in self:
            try:
                data = provider._obtain_rates(
                    provider.company_id.currency_id.name,
                    provider.currency_ids.mapped('name'),
                    date_from,
                    date_to
                ).items()
            except:
                e = exc_info()[1]
                _logger.warning(
                    'Currency Rate Provider "%s" failed to obtain data since'
                    ' %s until %s' % (
                        provider.name,
                        date_from,
                        date_to,
                    ),
                    exc_info=True,
                )
                provider.message_post(
                    subject=_('Currency Rate Provider Failure'),
                    body=_(
                        'Currency Rate Provider "%s" failed to obtain data'
                        ' since %s until %s:\n%s'
                    ) % (
                        provider.name,
                        date_from,
                        date_to,
                        str(e) if e else _('N/A'),
                    ),
                )
                continue

            if not data:
                if is_scheduled:
                    provider._schedule_next_run()
                continue
            if newest_only:
                data = [max(
                    data,
                    key=lambda x: fields.Date.from_string(x[0])
                )]

            for content_date, rates in data:
                timestamp = fields.Date.from_string(content_date)
                for currency_name, rate in rates.items():
                    if currency_name == provider.company_id.currency_id.name:
                        continue

                    currency = Currency.search([
                        ('name', '=', currency_name),
                    ], limit=1)
                    if not currency:
                        raise UserError(
                            _(
                                'Unknown currency from %(provider)s: %(rate)s'
                            ) % {
                                'provider': provider.name,
                                'rate': rate,
                            }
                        )
                    for idx, a in enumerate(rate):
                        rate[idx] = provider._process_rate(
                            currency,
                            a
                        )

                    record = CurrencyRate.search([
                        ('company_id', '=', provider.company_id.id),
                        ('currency_id', '=', currency.id),
                        ('name', '=', timestamp),
                    ], limit=1)
                    if record:
                        record.write({
                            'rate': rate[0],
                            'second_rate': rate[1],
                            'provider_id': provider.id,
                        })
                    else:
                        record = CurrencyRate.create({
                            'company_id': provider.company_id.id,
                            'currency_id': currency.id,
                            'name': timestamp,
                            'rate': rate[0],
                            'second_rate': rate[1],
                            'provider_id': provider.id,
                        })

            if is_scheduled:
                provider._schedule_next_run()