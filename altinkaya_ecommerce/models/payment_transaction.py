# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    # Callback_hash alanını yazarken erişim hatası alıyorduk. Çözüm olarak
    # base.group_system olan grup, account.group_account_invoice grubuna
    # çevrildi.
    callback_hash = fields.Char(groups="account.group_account_invoice")
