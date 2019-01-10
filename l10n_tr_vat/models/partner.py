# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo.tools.translate import _
import re
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    
    @api.constrains('vat')
    def check_vat(self):
        for partner in self:
            if partner.sanitized_vat == '11111111111' or partner.sanitized_vat == '2222222222' :
                return False
            if not partner.vat or partner.vat == "False":
                return False
            if partner.parent_id:
                return False
            colliding_partner = self.search([('sanitized_vat', '=', partner.sanitized_vat),('id', '!=', partner.id),('is_company', '=', 1)],limit=1)
            colliding_partner = self.browse(colliding_partner.id)
            if colliding_partner and colliding_partner.company_id.id == partner.company_id.id:
                if colliding_partner.commercial_partner_id != partner.commercial_partner_id:
                    raise UserError(_('The VAT number [%s] for this partner is also registered with partner [%s] Each partner should have unique vat number.') % (colliding_partner[0].vat,colliding_partner[0].name))
            else:
                self.check_vat_tr(partner.vat)
        return super(ResPartner,self).check_vat()



    @api.multi
    def write(self,values):
        if 'vat' in values:
            self.check_vat()
        return super(ResPartner,self).write(values)