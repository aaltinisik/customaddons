# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

import time
from datetime import date, datetime
from odoo.exceptions import ValidationError
from odoo import models, fields, api
from odoo.tools.translate import _


class Partner(models.Model):
    _inherit = "res.partner"

    # use_secondary_currency = fields.Boolean(string="Ekstrede çift para birimi yazdır",default=False)

    @api.multi
    def _get_statement_data_currency(self, data=None):
        return self._get_statement_data(self)

    @api.multi
    def _get_statement_data(self, data=None):
        statement_data2 = {}
        ctx = self._context.copy()
        currency_count = 0
        statement_data = []
        balance, seq = 0.0, 0
        currency_balance = 0.0
        Currency = self.env["res.currency"]
        end_date = ctx.get("date_end") or date(date.today().year, 12, 31)

        if date.today().month < 5:
            start_date = ctx.get("date_start") or date(date.today().year - 1, 1, 1)
        else:
            start_date = ctx.get("date_start") or date(date.today().year - 1, 1, 1)

        move_type = ("payable", "receivable")

        query = """SELECT L.DATE, A.CODE, A.CURRENCY_ID as ACCOUNT_CURRENCY,
    	AJ.NAME AS JOURNAL,	AM.NAME,INV.NUMBER, INV.SUPPLIER_INVOICE_NuMBER,L.MOVE_ID,L.DATE_MATURITY AS DUE_DATE,
    
    	CASE
    					WHEN INV.SUPPLIER_INVOICE_NuMBER IS NOT NULL THEN INV.SUPPLIER_INVOICE_NuMBER
    					ELSE INV.NUMBER
    	END AS INNUMBER,    
    
    	CASE
    					WHEN INV.NUMBER IS NOT NULL THEN AJ.NAME
    					ELSE AJ.NAME
    	END AS DESCIRIPTION,
        CASE
                        WHEN (SUM(L.DEBIT) - SUM(L.CREDIT)) > 0 THEN ROUND((SUM(L.DEBIT) - SUM(L.CREDIT)),2)
                        ELSE 0.00
        END AS DEBIT,
        CASE
                        WHEN SUM(L.DEBIT) - SUM(L.CREDIT) < 0 THEN -1 * ROUND((SUM(L.DEBIT) - SUM(L.CREDIT)),2)
                        ELSE 0.00
        END AS CREDIT,
        CASE
                        WHEN   ABS(SUM (L.AMOUNT_CURRENCY)) > 0 THEN  ROUND(ABS(SUM(L.DEBIT) - SUM(L.CREDIT))/ABS(SUM (L.AMOUNT_CURRENCY)),5)
                        ELSE 0.00
        END AS currency_rate,
        CASE
                        WHEN ROUND(SUM (L.AMOUNT_CURRENCY),4) > 0 THEN ROUND(SUM (L.AMOUNT_CURRENCY),4)
                        ELSE 0.00
        END AS DEBIT_currency,
        CASE
                        WHEN ROUND(SUM (L.AMOUNT_CURRENCY),4) < 0 THEN -1 * ROUND(SUM (L.AMOUNT_CURRENCY),4)
                        ELSE 0.00
        END AS CREDIT_currency,
        ROUND(SUM (L.AMOUNT_CURRENCY),4) AS AMOUNT_CURRENCY,AM.STATE,L.CURRENCY_ID AS CURRENCY_ID,
        L.COMPANY_CURRENCY_ID AS COMPANY_CURRENCY_ID,AJ.ID AS JOURNAL_ID,L.ACCOUNT_ID AS ACCOUNT_ID
        FROM ACCOUNT_MOVE_LINE AS L
        LEFT JOIN ACCOUNT_ACCOUNT A ON (L.ACCOUNT_ID = A.ID) LEFT JOIN ACCOUNT_MOVE AM ON (L.MOVE_ID = AM.ID)
        LEFT JOIN ACCOUNT_JOURNAL AJ ON (AM.JOURNAL_ID = AJ.ID) LEFT JOIN ACCOUNT_ACCOUNT_TYPE AT ON (A.USER_TYPE_ID = AT.ID)
        LEFT JOIN ACCOUNT_INVOICE INV ON (L.INVOICE_ID = INV.ID)
        WHERE (L.DATE BETWEEN '{0}' AND '{1}')
        AND L.PARTNER_ID = {2}
        AND AT.TYPE IN {3}
        GROUP BY AJ.NAME, A.CODE, A.CURRENCY_ID, L.MOVE_ID,	AM.NAME,	AM.STATE,	L.DATE,	L.DATE_MATURITY,	L.CURRENCY_ID,	L.COMPANY_CURRENCY_ID,
        INV.NUMBER,INV.SUPPLIER_INVOICE_NUMBER,	AJ.ID,	L.ACCOUNT_ID
        ORDER BY ACCOUNT_CURRENCY, L.DATE""".format(
            str(start_date),
            str(end_date),
            str(self.commercial_partner_id.id),
            str(move_type),
        )

        currency_difference_accounts = (
            self.env["account.account"]
            .search([("code", "in", ["646", "656", "646.F"])])
            .mapped("id")
        )
        currency_difference_to_invoice_journal = (
            self.env["account.journal"]
            .search([("code", "in", ["ADVR", "KRFRK"])])
            .mapped("id")
        )
        self.env.cr.execute(query)
        data = self.env.cr.dictfetchall()
        if len(data) == 0:
            raise ValidationError(_("No records found for your selection!"))
        onhand_currency_id = data[0]["account_currency"]
        for sl in data:

            if onhand_currency_id != sl["account_currency"]:
                currency_count += 1
                onhand_currency_id = sl["account_currency"]
                statement_data = []
                balance, seq = 0.0, 0
                currency_balance = 0.0

            if sl["journal_id"] in currency_difference_to_invoice_journal:
                ## pass move line if item in currency difference journal
                continue
            seq += 1
            if sl["account_id"] in currency_difference_accounts:
                # if line is currency difference currency values shall be cleared
                sl["currency_rate"] = 0.0
                sl["debit_currency"] = 0.0
                sl["credit_currency"] = 0.0
                sl["amount_currency"] = 0.0
                sl["currency_id"] = sl["company_currency_id"]

            balance = (sl["debit"] - sl["credit"]) + balance
            currency_balance = (
                sl["debit_currency"] - sl["credit_currency"]
            ) + currency_balance
            debit = 0.0
            credit = 0.0

            journal = self.env["account.journal"].browse(
                sl["journal_id"]).with_context(
                lang=self.commercial_partner_id.lang)

            if sl["innumber"]:
                description = journal.name + " " + sl["innumber"]
            else:
                description = journal.name
            company_currency_id = Currency.browse(sl["company_currency_id"])
            line_currency_id = Currency.browse(sl["currency_id"])
            if (sl["debit"] - sl["credit"]) > 0.0:
                debit = sl["debit"] - sl["credit"]
            else:
                credit = sl["credit"] - sl["debit"]

            statement_data.append(
                {
                    "seq": seq,
                    "number": sl["name"],
                    "date": sl["date"]
                    and datetime.strptime(str(sl["date"]), "%Y-%m-%d").strftime(
                        "%d.%m.%Y"
                    )
                    or False,
                    "due_date": sl["due_date"]
                    and datetime.strptime(str(sl["due_date"]), "%Y-%m-%d").strftime(
                        "%d.%m.%Y"
                    )
                    or False,
                    "description": len(description) >= 40
                    and description[0:40]
                    or description,
                    "debit": debit,
                    "credit": credit,
                    "account_code": sl["code"],
                    "account_currency": sl["account_currency"] or 31,
                    "amount": debit - credit,
                    "balance": abs(balance) or 0.0,
                    "credit_currency": sl["credit_currency"],
                    "debit_currency": sl["debit_currency"],
                    "amount_currency": sl["debit_currency"] - sl["credit_currency"],
                    "currency_rate": sl["currency_rate"],
                    "currency_balance": abs(currency_balance) or 0.0,
                    "currency_dc": currency_balance > 0.01 and "B" or "A",
                    "line_currency_id": line_currency_id["symbol"],
                    "dc": balance > 0.01 and "B" or "A",
                    "total": balance or 0.0,
                    "currency_symbol": company_currency_id["symbol"],
                }
            )
            statement_data2[currency_count] = statement_data
        return statement_data2

    def email_statement(
        self,
    ):
        data_model = self.env["ir.model.data"]
        template = data_model.get_object(
            "altinkaya_reports", "email_template_edi_send_statement"
        )
        mail_id = template.send_mail(self.id, force_send=True)
        return True
