from odoo import api, fields, models, tools, _


class CurrencyRate(models.Model):
    _inherit = "res.currency.rate"

    rate_inverse = fields.Float(digits=(12, 6), default=1.0, compute="_compute_rate_inverse",
                                help="The inverse rate of the currency")
    rate_inverse_second = fields.Float(digits=(12, 6), default=1.0, compute="_compute_rate_inverse",
                                       help="The inverse rate of the currency")

    @api.multi
    @api.depends('rate', 'second_rate')
    def _compute_rate_inverse(self):
        for rate in self:
            rate.rate_inverse = 1.0 / rate.rate
            rate.rate_inverse_second = 1.0 / rate.second_rate
