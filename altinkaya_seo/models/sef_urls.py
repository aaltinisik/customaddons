# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


"""
Well, odoo doesn't have any model for URL translations. So we need to create one.
"""


class SEFUrls(models.Model):
    _name = "sef.urls"
    _description = "Search Engine Friendly URLs"
