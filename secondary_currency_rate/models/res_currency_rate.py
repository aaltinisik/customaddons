from odoo import models, fields, api
import logging


_logger = logging.getLogger(__name__)


class ResCurrencyRateSecond(models.Model):
    _inherit = 'res.currency.rate'

    second_rate = fields.Float(digits=(12, 6),
                               default=1.0,
                               help='The second rate of the currency to the currency of rate 1')
