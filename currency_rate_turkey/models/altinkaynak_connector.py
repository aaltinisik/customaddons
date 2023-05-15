# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import requests
from datetime import datetime
from bs4 import BeautifulSoup


class AltinkaynakConnector:
    """
    Base class for altinkaynak.com connector
    """

    def __init__(self):
        self.endpoint = "https://www.altinkaynak.com/Doviz/Kur"
        self.main_data = {
            "ctl00$ctl00$ScriptManager1": "ctl00$ctl00$cphMain$cphSubContent$upValues|"
            "ctl00$ctl00$cphMain$cphSubContent$btnSearch",
            "ctl00$ctl00$cphMain$cphSubContent$dateInput": datetime.now().strftime(
                "%d/%m/%Y"
            ),
            "ctl00$ctl00$cphMain$cphSubContent$wccRange$CallbackState": "",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__ASYNCPOST: ": "true",
            "ctl00$ctl00$cphMain$cphSubContent$btnSearch": "Getir",
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "X-MicrosoftAjax": "Delta=true",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.cookies = None
        self.main_data.update(self._get_tokens())

    def _get_tokens(self):
        """
        Get tokens from altinkaynak.com
        :return:
        """
        resp = requests.get(self.endpoint, headers=self.headers)

        # Set cookies
        self.cookies = resp.cookies

        soup = BeautifulSoup(resp.content, "html.parser")
        return {
            "cphMain_cphSubContent_pcHintWS": soup.find(
                "input", attrs={"id": "cphMain_cphSubContent_pcHintWS"}
            ).attrs["value"],
            "__VIEWSTATE": soup.find("input", attrs={"id": "__VIEWSTATE"}).attrs[
                "value"
            ],
            "__VIEWSTATEGENERATOR": soup.find(
                "input", attrs={"id": "__VIEWSTATEGENERATOR"}
            ).attrs["value"],
        }

    def _get_rate(self, currencies, date):
        """
        Currency rate get from altinkaynak.com
        :param currency: EUR, USD, GBP, etc. (single)
        :param date: "dd/mm/yyyy" format
        :return:
        """
        self.main_data["ctl00$ctl00$cphMain$cphSubContent$dateInput"] = date
        response = requests.post(
            self.endpoint,
            data=self.main_data,
            cookies=self.cookies,
            headers=self.headers,
        )
        soup = BeautifulSoup(response.content, "html.parser")
        res = {}
        for currency in currencies:
            res[currency] = {
                "AltinkaynakBuying": 1 / float(soup.find("td", attrs={"id": f"td{currency.upper()}Buy"}).next),
                "AltinkaynakSelling": 1 / float(soup.find("td", attrs={"id": f"td{currency.upper()}Sell"}).next),
            }
        return res
