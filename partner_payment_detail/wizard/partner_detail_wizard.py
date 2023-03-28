# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today Acespritech Solutions Pvt Ltd
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
from odoo import fields, models, api
import time
from io import BytesIO
import xlwt
import base64


class wizard_partner_detail(models.TransientModel):
    _name = "wizard.partner.detail"
    _description = "Partner Details"

    start_date = fields.Date(
        "Start Date", required=True, default=lambda *a: time.strftime("%Y-01-01")
    )
    end_date = fields.Date(
        "End Date", required=True, default=lambda *a: time.strftime("%Y-%m-%d")
    )

    @api.multi
    def print_report(self):
        record = self
        ResPartner = self.env["res.partner"]
        partners = ResPartner.search([('parent_id', '=', False)])
        self.env.cr.execute(
            """SELECT l.partner_id, at.type, SUM(l.debit-l.credit)
                      FROM account_move_line l
                      LEFT JOIN account_account a ON (l.account_id=a.id)
                      JOIN account_account_type at ON (a.user_type_id =at.id)
                      WHERE at.type IN ('receivable','payable')
                      AND l.partner_id in %s
                      AND l.date >= %s
                      AND l.date <= %s
                      GROUP BY l.partner_id, at.type""",
            (tuple(partners.ids), record.start_date, record.end_date),
        )
        result = {}
        aml_dict = self.env.cr.fetchall()

        for partner_id in partners.filtered(lambda p: p.id in [x[0] for x in aml_dict]):
            result[partner_id] = {"receivable": 0, "payable": 0}
        for pid, acc_type, val in aml_dict:
            partner = ResPartner.browse(pid)
            if partner:
                result[partner][acc_type] = (acc_type == "receivable") and val or -val

        fl = BytesIO()
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("Customer Payment Details")
        sheet.write(0, 0, "Customer Name")
        sheet.write(0, 1, "Phone")
        sheet.write(0, 2, "Credit")
        sheet.write(0, 3, "Debit")
        sheet.write(0, 4, "Balance")
        #         sheet.write(0, 5, "Alicilar Kodu")
        #         sheet.write(0, 6, "Saticilar kodu")
        sheet.write(0, 7, "Faks")
        sheet.write(0, 8, "Vergi No")
        sheet.write(0, 9, "Vergi Daire")
        sheet.write(0, 10, "Adres1")
        sheet.write(0, 11, "Adres2")
        sheet.write(0, 12, "ilce")
        sheet.write(0, 13, "il")
        sheet.write(0, 14, "ulke")
        sheet.write(0, 15, "zirve borc hs.")
        sheet.write(0, 16, "zirve alacak hs.")
        row = 1
        for res in result.items():
            partner = res[0]
            if not partner.is_company:
                continue
            sheet.write(row, 0, partner.name)
            sheet.write(row, 1, partner.phone or "")
            sheet.write(row, 2, res[1]["payable"])
            sheet.write(row, 3, res[1]["receivable"])
            sheet.write(row, 4, res[1]["receivable"] - res[1]["payable"])
            #             sheet.write(row, 5, partner.z_receivable_export or '')
            #             sheet.write(row, 6, partner.z_payable_export or '')
            sheet.write(row, 7, partner.fax or "")
            sheet.write(row, 8, partner.vat or "")
            sheet.write(row, 9, partner.tax_office_name or "")
            sheet.write(row, 10, partner.street or "")
            sheet.write(row, 11, partner.street2 or "")
            sheet.write(row, 12, partner.city or "")
            sheet.write(row, 13, partner.state_id.name or "")
            sheet.write(row, 14, partner.country_id.name or "")
            sheet.write(row, 15,  partner.z_payable_export or "")
            sheet.write(row, 16, partner.z_receivable_export or "")
            row += 1
        wbk.save(fl)
        fl.seek(0)
        buffer = base64.encodebytes(fl.read())
        ctx = dict(self.env.context)
        ctx.update({"file": buffer})
        form_id = self.env["ir.model.data"].get_object_reference(
            "partner_payment_detail", "customer_excel_form"
        )[1]
        return {
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "customer.excel",
            "views": [(form_id, "form")],
            "view_id": form_id,
            "target": "new",
            "context": ctx,
        }


class CustomerExcel(models.Model):
    _name = "customer.excel"
    _description = "Customer Excel"

    @api.model
    def default_get(self, fields):
        res = super(CustomerExcel, self).default_get(fields)
        if self.env.context.get("file"):
            res.update(
                {"file": self.env.context["file"], "name": "Customer_Detail.xls"}
            )
        return res

    file = fields.Binary("File")
    name = fields.Char(string="File Name", size=64)

    @api.multi
    def download_xlsx(self):
        return {
            "name": "Report",
            "type": "ir.actions.act_url",
            "url": "web/content/?model="
            + self._name
            + "&id="
            + str(self.id)
            + "&filename_field=file_name&field=file&download=true&filename="
            + str(self.name),
            "target": "new",
        }
