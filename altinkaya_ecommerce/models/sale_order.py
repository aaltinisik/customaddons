# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    order_state = fields.Selection(
        [
            ("draft", "Taslak"),
            ("sent", "Teklif Gönderildi"),
            ("sale", "Satış Siparişi"),
            ("molding_waiting", "Kalıphanede Bekliyor"),
            ("molding", "Kalıphanede"),
            ("injection_waiting", "Enjeksiyonda Bekliyor"),
            ("injection", "Enjeksiyonda"),
            ("metal_waiting", "Preshane Bekliyor"),
            ("metal", "Preshane"),
            ("cnc_lathe_waiting", "CNC Torna Bekliyor"),
            ("cnc_lathe", "CNC Torna"),
            ("cnc_waiting", "CNC Bekliyor"),
            ("cnc", "CNC Kesimde"),
            ("uv_printing_waiting", "Görsel Baskıda Bekliyor"),
            ("uv_printing", "Görsel Baskıda"),
            ("assembly_waiting", "Montajda Bekliyor"),
            ("assembly", "Montajda"),
            ("at_warehouse", "Depoda"),
            ("on_transit", "Nakliyede"),
            ("delivered", "Teslim Edildi"),
            ("completed", "Tamamlandı"),
            ("cancel", "İptal"),
        ],
        string="Sipariş Durumu",
        readonly=True,
        copy=False,
        default="draft",
        index=True,
    )
