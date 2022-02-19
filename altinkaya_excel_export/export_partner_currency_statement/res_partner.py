from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    has_secondary_curr = fields.Boolean(string='Dövizle çalışıyor', default=False)
    secondary_curr_id = fields.Many2one('res.currency', string='Döviz birimi')
