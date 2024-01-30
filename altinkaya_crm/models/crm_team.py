# Copyright 2024 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models
import random


class CRMTeam(models.Model):
    _inherit = "crm.team"

    def _get_random_sales_person(self):
        """
        Returns a random sales person
        :return: res.users
        """
        return random.choice(self.member_ids).id
