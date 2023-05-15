# Copyright 2021 Yiğit Budak (https://github.com/yibudak)
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from sys import exc_info
from odoo.exceptions import UserError
from odoo.addons.currency_rate_turkey.models.res_currency_rate import RATE_FIELD_MAPPING


_logger = logging.getLogger(__name__)


class ResCurrencyRateProviderSecondRate(models.Model):
    _inherit = "res.currency.rate.provider"

    @api.multi
    def _update(self, date_from, date_to, newest_only=False):
        Currency = self.env["res.currency"]
        CurrencyRate = self.env["res.currency.rate"]
        is_scheduled = self.env.context.get("scheduled")
        for provider in self:
            try:
                data = provider._obtain_rates(
                    provider.company_id.currency_id.name,
                    provider.currency_ids.mapped("name"),
                    date_from,
                    date_to,
                ).items()
            except:
                e = exc_info()[1]
                _logger.warning(
                    'Currency Rate Provider "%s" failed to obtain data since'
                    " %s until %s"
                    % (
                        provider.name,
                        date_from,
                        date_to,
                    ),
                    exc_info=True,
                )
                provider.message_post(
                    subject=_("Currency Rate Provider Failure"),
                    body=_(
                        'Currency Rate Provider "%s" failed to obtain data'
                        " since %s until %s:\n%s"
                    )
                    % (
                        provider.name,
                        date_from,
                        date_to,
                        str(e) if e else _("N/A"),
                    ),
                )
                continue

            if not data:
                if is_scheduled:
                    provider._schedule_next_run()
                continue
            if newest_only:
                data = [max(data, key=lambda x: fields.Date.from_string(x[0]))]

            for content_date, rates in data:
                timestamp = fields.Date.from_string(content_date)
                for currency_name, rates_dict in rates.items():
                    if currency_name == provider.company_id.currency_id.name:
                        continue

                    currency = Currency.search(
                        [
                            ("name", "=", currency_name),
                        ],
                        limit=1,
                    )
                    if not currency:
                        raise UserError(
                            _("Unknown currency from %(provider)s: %(rate)s")
                            % {
                                "provider": provider.name,
                                "rate": rates_dict,
                            }
                        )
                    for rate_type, rate in rates_dict.items():
                        rate = provider._process_rate(currency, rate)
                        is_main_rate = (
                            RATE_FIELD_MAPPING[rate_type] == currency.main_rate_field
                        )
                        record = CurrencyRate.search(
                            [
                                ("company_id", "=", provider.company_id.id),
                                ("currency_id", "=", currency.id),
                                ("name", "=", timestamp),
                            ],
                            limit=1,
                        )
                        if record:
                            vals = {
                                RATE_FIELD_MAPPING[rate_type]: rate,
                                "provider_id": provider.id,
                            }
                            if is_main_rate:
                                vals["rate"] = rate
                            record.write(vals)
                        else:
                            vals = {
                                "company_id": provider.company_id.id,
                                "currency_id": currency.id,
                                "name": timestamp,
                                RATE_FIELD_MAPPING[rate_type]: rate,
                                "provider_id": provider.id,
                            }
                            if is_main_rate:
                                vals["rate"] = rate
                            record = CurrencyRate.create(vals)

            if is_scheduled:
                provider._schedule_next_run()
