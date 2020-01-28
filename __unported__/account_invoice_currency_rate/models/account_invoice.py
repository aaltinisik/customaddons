# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def _default_currency_rate(self):
        currency = self._default_currency()
        return currency.rate or 1.0

    use_currency_rate = fields.Boolean('Use Policy', compute='_compute_use_currency_rate')

    currency_rate_type_id = fields.Many2one(
        'res.currency.rate.type',
        'Currency Rate Type',
        compute='_compute_currency_rate_type',
        readonly=True,
        store=True,
        states={'draft': [('readonly', False)]},
        help="Currency rate type of this invoice",
    )

    currency_rate = fields.Float(
        string='Currency Rate',
        digits=(12, 6),
        required=True,
        readonly=True,
        default=_default_currency_rate,
        states={'draft': [('readonly', False)]},
        compute='_compute_currency_rate',
        inverse='_inverse_currency_rate',
        help="Currency rate of this invoice",
    )

    use_custom_rate = fields.Boolean(
        'Custom Rate',
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=False)

    custom_rate = fields.Float(
        string='Custom Rate',
        digits=(12, 6),
        readonly=True,
        default=_default_currency_rate,
    )

    amount_total_company_currency = fields.Float(
        string='Company Currency Total',
        digits=dp.get_precision('Account'),
        readonly=True,
        compute='_compute_amount_total_company_currency',
        help="Total in company currency",
    )

    @api.one
    @api.depends('currency_id', 'company_id.currency_id')
    def _compute_use_currency_rate(self):
        self.use_currency_rate = self.currency_id and self.currency_id != self.company_id.currency_id

    @api.one
    @api.depends('currency_id', 'currency_rate_type_id', 'use_currency_rate',
                 'use_custom_rate', 'custom_rate', 'date_invoice')
    def _compute_currency_rate(self):
        if self.use_custom_rate:
            self.currency_rate = self.custom_rate
        else:
            rate = self.env['res.currency']._get_currency_rate_for_date(
                self.currency_id, self.date_invoice, self.currency_rate_type_id, self.company_id)
            self.currency_rate = rate or self.currency_id.rate

    @api.one
    @api.depends('partner_id', 'use_currency_rate')
    def _compute_currency_rate_type(self):
        if self.partner_id and self.use_currency_rate:
            if self.type in ('out_invoice', 'out_refund'):
                self.currency_rate_type_id = self.partner_id.customer_currency_rate_type_id
            else:
                self.currency_rate_type_id = self.partner_id.supplier_currency_rate_type_id
        else:
            self.currency_rate_type_id = False

    @api.one
    def _inverse_currency_rate(self):
        self.custom_rate = self.currency_rate

    @api.one
    @api.depends('amount_total', 'currency_rate')
    def _compute_amount_total_company_currency(self):
        if self.use_currency_rate:
            self.amount_total_company_currency = self.amount_total * self.currency_rate
        else:
            self.amount_total_company_currency = self.amount_total

    @api.multi
    def action_move_create(self):
        return super(AccountInvoice, self.with_context(
            currency_rate_type_id=self.currency_rate_type_id,
            use_custom_rate=self.use_custom_rate,
            custom_rate=self.custom_rate,
            use_currency_rate=self.use_currency_rate,
            rate_date=self.date_invoice,
            company_id=self.company_id)).action_move_create()
