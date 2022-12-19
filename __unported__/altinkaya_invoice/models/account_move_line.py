from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    move_name = fields.Char(related='move_id.name', string='Move Number')
    move_ref = fields.Char(related='move_id.ref', string='Move Reference')
    journal_id = fields.Many2one('account.journal', related='move_id.journal_id', string='Journal')
