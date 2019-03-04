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

import datetime

from dateutil.relativedelta import relativedelta
from odoo import fields
from odoo import tools
from odoo.tests.common import TransactionCase
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class TestAccountFollowup(TransactionCase):
    def setUp(self):
        """ setUp ***"""
        super(TestAccountFollowup, self).setUp()

        self.user = self.env['res.users']
        self.user_id = self.env.user
        self.partner = self.env['res.partner']
        self.invoice = self.env['account.invoice']
        self.invoice_line = self.env['account.invoice.line']
        self.wizard = self.env['devit_account_followup.print']
        self.followup_id = self.env['devit_account_followup.followup']
        self.main_company = self.env.ref('base.main_company')

        self.account_user_type = self.env.ref(
            'account.data_account_type_receivable')
        self.account_id = self.env['account.account'].create(
            {'code': 'X1012', 'name': 'Debtors - (test)',
             'reconcile': True, 'company_id': self.main_company.id,
             'user_type_id': self.account_user_type.id})
        self.partner_id = self.partner.create(
            {'name': 'Test Company',
             'email': 'test@localhost',
             'is_company': True,
             'property_account_receivable_id': self.account_id.id,
             'property_account_payable_id': self.account_id.id,
             })

        self.followup_id = self.env.ref("devit_account_followup.demo_followup1")
        self.journal_id = self.env['account.journal'].search(
            [('type', '=', 'bank')], limit=1)
        self.pay_account_id = self.env['account.journal'].search(
            [('type', '=', 'cash')], limit=1)
        self.payment_term = self.env.ref(
            'account.account_payment_term_immediate')
        self.first_followup_line_id = self.env.ref(
            "devit_account_followup.demo_followup_line1")
        self.last_followup_line_id = self.env.ref(
            "devit_account_followup.demo_followup_line3")
        self.product_id = self.env.ref("product.product_product_6")
        self.journal = self.env['account.journal'].create(
            {'name': 'Customer Invoices - Test', 'code': 'TINV',
             'type': 'sale', 'default_credit_account_id': self.account_id.id,
             'default_debit_account_id': self.account_id.id,
             'refund_sequence': True})
        self.journalrec = self.journal and self.journal[0] or False
        self.invoice_line = [
            (0, 0, {
                'product_id': self.env.ref('product.product_product_5').id,
                'quantity': 10.0,
                'account_id': self.account_id.id,
                'name': 'product test 5',
                'price_unit': 100.00, })
        ]
        self.invoice_id = self.invoice.sudo(self.env.user.id).create(
            dict(name="Test Customer Invoice",
                 reference_type="none",
                 payment_term_id=self.payment_term.id,
                 journal_id=self.journalrec.id,
                 partner_id=self.partner_id.id,
                 account_id=self.account_id.id,
                 invoice_line_ids=self.invoice_line
                 ))
        self.invoice_id.action_invoice_open()
        self.current_date = datetime.datetime.strptime(
            fields.Date.today(), DEFAULT_SERVER_DATE_FORMAT)

    def test_00_send_followup_after_3_days(self):
        """ Send follow up after 3 days and check nothing is done
        (as first follow-up level is only after 15 days)"""
        delta = datetime.timedelta(days=3)
        result = self.current_date + delta
        self.wizard_id = self.wizard.with_context(
            {"followup_id": self.followup_id.id}).create(
            {'date': result.strftime(tools.DEFAULT_SERVER_DATE_FORMAT),
             'followup_id': self.followup_id.id
             })
        self.wizard_id.with_context(
            {"followup_id": self.followup_id.id}).do_process()
        self.assertFalse(self.partner_id.latest_followup_level_id)

    def run_wizard_three_times(self):
        result = self.current_date + relativedelta(days=40)
        self.wizard_id = self.wizard.with_context(
            {"followup_id": self.followup_id.id}).create(
            {'date': result.strftime(tools.DEFAULT_SERVER_DATE_FORMAT),
             'followup_id': self.followup_id.id})
        self.wizard_id.with_context(
            {"followup_id": self.followup_id.id}).do_process()
        self.partner_id._get_latest()
        self.wizard_id = self.wizard.create(
            {'date': result.strftime(tools.DEFAULT_SERVER_DATE_FORMAT),
             'followup_id': self.followup_id.id})
        self.wizard_id.with_context(
            {"followup_id": self.followup_id.id}).do_process()
        self.partner_id._get_latest()
        self.wizard_id = self.wizard.with_context(
            {"followup_id": self.followup_id.id}).create(
            {'date': result.strftime(tools.DEFAULT_SERVER_DATE_FORMAT),
             'followup_id': self.followup_id.id})
        self.wizard_id.with_context(
            {"followup_id": self.followup_id.id}).do_process()
        self.partner_id._get_latest()

    def test_01_send_followup_later_for_upgrade(self):
        """ Send one follow-up after 15 days to check it upgrades to level 1"""
        result = self.current_date + relativedelta(days=15)
        self.wizard_id = self.wizard.with_context(
            {"followup_id": self.followup_id.id}).create(
            {'date': result.strftime(tools.DEFAULT_SERVER_DATE_FORMAT),
             'followup_id': self.followup_id.id})
        self.wizard_id.with_context(
            {"followup_id": self.followup_id.id}).do_process()
        self.partner_id._get_latest()
        self.assertEqual(self.partner_id.latest_followup_level_id.id,
                         self.first_followup_line_id.id,
                         "Not updated to the correct follow-up level")

    def test_02_check_manual_action(self):
        """ Check that when running the wizard three times
        that the manual action is set"""
        self.run_wizard_three_times()
        self.assertEqual(self.partner_id.latest_followup_level_id.name,
                         "Call the customer on the phone",
                         "Manual action not set")
        self.assertEqual(
            self.partner_id.payment_next_action_date,
            self.current_date.strftime(tools.DEFAULT_SERVER_DATE_FORMAT))

    def test_03_action_done(self):
        """ Run the wizard 3 times, mark it as done,
        check the action fields are empty"""
        partner_rec = self.partner_id
        self.run_wizard_three_times()
        self.partner_id.action_done()
        self.assertFalse(partner_rec.payment_next_action,
                         "Manual action not emptied")
        self.assertFalse(partner_rec.payment_responsible_id,
                         "Payment responsible not emptied")
        self.assertFalse(partner_rec.payment_next_action_date,
                         "Next action date not emptied")

    def test_04_litigation(self):
        """ Set the account move line as litigation, run the wizard 3
        times and check nothing happened.
        Turn litigation off.  Run the wizard 3 times and check it is
        in the right follow-up level.
        """
        # aml_id = self.partner_id.unreconciled_aml_ids[0].id
        aml_id = \
            self.partner_id.unreconciled_aml_ids and \
            self.partner_id.unreconciled_aml_ids[0]
        aml_id.write({'blocked': True})
        self.run_wizard_three_times()
        self.assertFalse(self.partner_id.latest_followup_level_id,
                         "Litigation does not work")
        aml_id.write({'blocked': False})
        self.run_wizard_three_times()
        self.assertEqual(self.partner_id.latest_followup_level_id.id,
                         self.last_followup_line_id.id, "Lines are not equal")

    def test_05_pay_the_invoice(self):
        """Run wizard until manual action, pay the invoice and check that
        partner has no follow-up level anymore and after running the wizard
        the action is empty"""
        self.test_02_check_manual_action()
        self.partner_id._get_latest()
        result = self.current_date + relativedelta(days=1)
        self.wizard_id = self.wizard.with_context(
            {"followup_id": self.followup_id.id}).create(
            {'date': result.strftime(tools.DEFAULT_SERVER_DATE_FORMAT),
             'followup_id': self.followup_id.id})
        self.wizard_id.with_context(
            {"followup_id": self.followup_id.id}).do_process()
        self.partner_id._get_latest()
        self.assertEqual(0, self.partner_id.payment_amount_due,
                         "Amount Due != 0")
