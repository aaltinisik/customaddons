# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, api, fields


class CRMClaimMapping(models.AbstractModel):
    _name = "crm.claim.mapping"
    _description = "Base model for CRM Claim - Odoo models integration"

    crm_claim_ids = fields.Many2many('crm.claim', string='Claims')
    crm_claim_count = fields.Integer(compute='_compute_claims_count',
                                     store=True,
                                     string='Claim Count')

    @api.depends('crm_claim_ids')
    @api.multi
    def _compute_claims_count(self):
        for rec in self:
            rec.crm_claim_count = len(rec.crm_claim_ids)

    @api.multi
    def action_view_claims(self):
        claims = self.mapped('crm_claim_ids')
        action = self.env.ref('crm_claim.crm_claim_category_claim0').read()[0]
        form_view = [(self.env.ref('crm_claim.crm_case_claims_form_view').id,
                      'form')]
        if len(claims) > 1:
            action['domain'] = [('id', 'in', claims.ids)]
            return action

        else:
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in
                                               action['views'] if
                                               view != 'form']
            else:
                action['views'] = form_view

            if claims:
                action['res_id'] = claims.ids[0]
            else:
                action["context"] = {
                    "default_model_ref_id": "%s,%s" % (self._name, self.id)}
        return action


class CRMClaimSaleOrderMixin(models.Model):
    _name = "sale.order"
    _inherit = ['sale.order', 'crm.claim.mapping']


class CRMClaimInvoiceMixin(models.Model):
    _name = "account.invoice"
    _inherit = ['account.invoice', 'crm.claim.mapping']


class CRMClaimPickingMixin(models.Model):
    _name = "stock.picking"
    _inherit = ['stock.picking', 'crm.claim.mapping']


class CRMClaimProductMixin(models.Model):
    _name = "product.product"
    _inherit = ['product.product', 'crm.claim.mapping']
