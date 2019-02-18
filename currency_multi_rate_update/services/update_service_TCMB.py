# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2014 Eska Yazilim (<http://www.eskayazilim.com.tr>).
#    @author Levent Karakaş
#
#    Abstract class to fetch rates from Turkish National Central Bank
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
from .currency_getter_interface import CurrencyGetterInterface


from datetime import datetime

import logging
_logger = logging.getLogger(__name__)


class TCMBGetter(CurrencyGetterInterface):
    """Implementation of Currency_getter_factory interface
    for TCMB service
    """

    code = 'TCMB'
    name = 'Türkiye Cumhuriyet Merkez Bankası'
    supported_currency_array = [
        "AUD", "CAD", "CHF", "DKK", "EUR", "GBP", "JPY", "KWD", "NOK", "SAR",
        "SEK", "USD","TRY"]


    def rate_retrieve(self, dom, ns, curr, type):
        """Parse a dom node to retrieve-
        currencies data

        """
        res = {}
        if type == 'forex_buy':
            xpath_curr_rate = ("./Currency[@Kod='%s']/ForexBuying") % (curr.upper())
        elif type == 'forex_sell':
            xpath_curr_rate = ("./Currency[@Kod='%s']/ForexSelling") % (curr.upper())
        elif type == 'banknote_buy':
            xpath_curr_rate = ("./Currency[@Kod='%s']/BanknoteBuying") % (curr.upper())
        elif type == 'banknote_sell':
            xpath_curr_rate = ("./Currency[@Kod='%s']/BanknoteSelling") % (curr.upper())
        res['rate_currency'] = float(
            dom.findall(xpath_curr_rate)[0].text
        )
        xpath_rate_ref = ("./Currency[@Kod='%s']/Unit") % (curr.upper())
        res['rate_ref'] = float(dom.findall(xpath_rate_ref)[0].text)
        return res

    def get_updated_currency(self, currency_array, main_currency,
                             max_delta_days):
        """implementation of abstract method of Curreny_getter_interface"""
        url = 'http://www.tcmb.gov.tr/kurlar/today.xml'
        # Important : as explained on the TCMB web site, the currencies are
        # at the beginning of the afternoon ; so, until 15:30 Turkish local time (GMT+2)
        # the currency rates are the ones of trading day N-1

        # We do not want to update the main currency
        if main_currency in currency_array:
            currency_array.remove(main_currency)
#         from lxml.ElementInclude import etree
        import xml.etree.ElementTree as ET
        _logger.debug("TCMB currency rate service : connecting...")
        rawfile = self.get_url(url)
#         dom = etree.fromstring(rawfile)
        dom = ET.fromstring(rawfile)
        ns = {}
        _logger.debug("TCMB sent a valid XML file")

        rate_date = dom.get('Date')

        rate_date_datetime = datetime.strptime(rate_date, "%m/%d/%Y")
        self.check_rate_date(rate_date_datetime, max_delta_days)

        # We dynamically update supported currencies
        
        #self.supported_currency_array = dom.xpath(
        #    "/Tarih_Date/Currency@Kod",
        #    namespaces=ns
        #)
        #self.supported_currency_array.append('TRY')
        #_logger.debug("Supported currencies = %s " %
        #              self.supported_currency_array)
        #self.validate_cur(main_currency)

        for type in ('forex_buy', 'forex_sell', 'banknote_buy', 'banknote_sell'):
            if main_currency != 'TRY':
                main_curr_data = self.rate_retrieve(dom, ns, main_currency, type)
                main_rate = (main_curr_data['rate_currency'] /
                                main_curr_data['rate_ref'])
            for curr in currency_array:
                self.validate_cur(curr)
                if curr == 'TRY':
                    rate = main_rate
                else:
                    curr_data = self.rate_retrieve(dom, ns, curr, type)
                    if not curr_data['rate_ref']:
                        continue
                    if main_currency == 'TRY':
                        rate = curr_data['rate_ref'] / curr_data['rate_currency']
                    else:
                        rate = (main_rate * curr_data['rate_ref'] /
                                curr_data['rate_currency'])
                self.updated_currency[curr+(type or '')] = rate
                _logger.debug(
                    "Rate retrieved : 1 %s = %s %s" % (main_currency, rate, curr)
                )
        return self.updated_currency, self.log_info


