from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # default_currency_provider_type = fields.Selection([
    #     ('ForexBuying', _('Forex Buy')),
    #     ('ForexSelling', _('Forex Sell')),
    #     ('BanknoteBuying', _('Banknote Buy')),
    #     ('BanknoteSelling', _('Banknote Sell'))], string='Service Rate Type')
    #
    use_second_rate_type = fields.Boolean(string='Use Secondary Provider Type', default=False)
