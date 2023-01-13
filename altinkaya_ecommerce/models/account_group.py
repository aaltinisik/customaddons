# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class AccountGroup(models.Model):
    _inherit = "account.group"

    # """We can use any length of prefix. So we are disabling the constraint."""
    # _sql_constraints = [
    #     ("check_length_prefix", "check(1=1)", "No error"),
    # ]
    #
    # def _search_code_prefix(self, operator, value):
    #     prefix = value.split(".")
    #     domain = [("code_prefix_start", "=", prefix[0])]
    #     if len(prefix) > 1:
    #         domain.append(("code_prefix_end", "=", prefix[1]))
    #     records = self.search(domain)
    #     res = records.ids if len(records) > 1 else records.id
    #     return [("id", operator, res)]
    #
    # code_prefix = fields.Char(
    #     string="Code Prefix",
    #     compute="_compute_code_prefix",
    #     search="_search_code_prefix",
    # )
    #
    @api.constrains("code_prefix_start", "code_prefix_end")
    def _constraint_prefix_overlap(self):
        """Overriding the method to prevent the error
        "Account Groups with the same granularity can't overlap"
        We don't need this constraint in our case."""
        return True

    def name_get(self):
        """Originally the name_get method returns the codes "-" in between.
        We replace them with dot."""
        res = super(AccountGroup, self).name_get()
        return [(r[0], r[1].replace("-", ".")) for r in res]

    @api.model_create_multi
    def create(self, vals_list):
        """/addons/account/models/account_account.py line 853.
         We don't need to fill code_prefix_end"""
        res_ids = super(AccountGroup, self).create(vals_list)
        for rec in res_ids:
            if rec.code_prefix_start == rec.code_prefix_end:
                rec.code_prefix_end = ''
        return res_ids

    # def _compute_code_prefix(self):
    #     """In version 12.0 we write the code_prefix field manually
    #     (with a dot in between).This method is for compute code_prefix
    #      field to match the account.group model in connector imports."""
    #     for rec in self:
    #         rec.code_prefix = rec.code_prefix_start
    #         if rec.code_prefix_end:
    #             rec.code_prefix += "." + rec.code_prefix_end
    #     return True
