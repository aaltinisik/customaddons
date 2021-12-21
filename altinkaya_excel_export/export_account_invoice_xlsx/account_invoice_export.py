# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields,models,api


class ReportAccountInvoice(models.TransientModel):
    _name = 'report.account.invoice'
    _description = 'Wizard for report.account.invoice'
    _inherit = 'xlsx.report'

    # Report Result, account.invoice
    results = fields.Many2many(
        comodel_name='account.invoice',
        string='Invoices',
        compute='_get_invoices',
        help='Use compute fields, so there is nothing stored in database',
    )

    @api.multi
    @api.depends('results')
    def _get_invoices(self):
        selected_ids = self.env.context.get('active_ids', [])
        ids = self.env['account.invoice'].browse(selected_ids)
        for rec in self:
            rec.results = ids
