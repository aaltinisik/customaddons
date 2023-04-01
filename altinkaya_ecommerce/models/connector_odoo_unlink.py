# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api


class ConnectorOdooUnlink(models.TransientModel):
    _name = "connector.odoo.unlink"
    _description = "Connector Odoo Unlink"

    def check_existing_bindings(self, model_name, ids):
        """
        Check if there are any bindings for the given ids.
        model: model name of the binding
        ids: list of ids to check
        :returns list of ids to unlink
        """
        model = self.env[model_name]
        unlink_ids = []

        records = model.search([("id", "in", ids)])
        exist_ids = records.ids
        for odoo_id in ids:
            if odoo_id not in exist_ids:
                unlink_ids.append(odoo_id)

        return unlink_ids
