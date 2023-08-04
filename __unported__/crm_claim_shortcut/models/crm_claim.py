# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields
from odoo.addons.crm_claim.models.crm_claim import APPLICABLE_MODELS

APPLICABLE_MODELS.append('stock.picking')  # Add stock.picking to model_ref_id


class CRMClaim(models.Model):
    _inherit = 'crm.claim'

    source_id = fields.Many2one('utm.source', string='Source')
    carrier_id = fields.Many2one('delivery.carrier', string='Carrier')

    @api.model
    def create(self, vals):
        res = super(CRMClaim, self).create(vals)
        for rec in res.filtered(lambda x: x.model_ref_id):
            rec.model_ref_id.crm_claim_ids = [(4, rec.id)]
        return res

    @api.multi
    def unlink(self):
        for rec in self:
            rec.model_ref_id.crm_claim_ids = [(3, rec.id)]
        return super(CRMClaim, self).unlink()
