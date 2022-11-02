# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models
from odoo.addons.crm_claim.models.crm_claim import APPLICABLE_MODELS

APPLICABLE_MODELS.append('stock.picking')  # Add stock.picking to model_ref_id


class CRMClaim(models.Model):
    _inherit = 'crm.claim'

    @api.model
    def create(self, vals):
        res = super(CRMClaim, self).create(vals)
        res.model_ref_id.crm_claim_ids = [(4, res.id)]
        return res
