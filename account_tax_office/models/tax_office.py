# -*- encoding: utf-8 -*-
from odoo import models, fields


class TaxOffice(models.Model):
    _name = "account.tax.office"
    _description = "Tax Office"
    _order = "state_id"

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Tax Office Name", required=True)
    code = fields.Char(string="Tax Office Code", size=6)
    state_id = fields.Many2one('res.country.state',
                               string="County/State", required=True)


class ResPartnerTaxOffice(models.Model):
    _inherit = 'res.partner'

    tax_office_id = fields.Many2one('account.tax.office',
                                    string="Tax Office",
                                    ondelete='restrict')


class ResCompanyTaxOffice(models.Model):
    _inherit = "res.company"

    tax_office_id = fields.Many2one(related="partner_id.tax_office_id",
                                    string="Tax Office")
