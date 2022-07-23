# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields,models,api


class ReportAccountMoveLine(models.TransientModel):
    _name = 'report.account.move.line'
    _description = 'Wizard for report.account.move.line'
    _inherit = 'xlsx.report'

    # Report Result, account.move.line
    results = fields.Many2many(
        comodel_name='account.move.line',
        string='Move Lines',
        compute='_get_move_lines',
        help='Use compute fields, so there is nothing stored in database',
    )

    @api.multi
    def _get_move_lines(self):
        selected_ids = self.env.context.get('active_ids', [])
        ids = self.env['account.move.line'].browse(selected_ids)
        for rec in self:
            rec.results = ids
