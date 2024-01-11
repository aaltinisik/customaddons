# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo.tools.translate import _
import re
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    
    @api.constrains('vat')
    def check_vat(self):
        # return True
        for partner in self:
            if partner.vat == '11111111111' or partner.vat == '2222222222':
                return False
            if not partner.vat or partner.vat == "False":
                return False
            if partner.parent_id:
                return
            if partner.country_id.code != 'TR' and self._context.get("connector_request"):
                return
            colliding_partner = self.search([('vat', '=', partner.vat),('id', '!=', partner.id),('is_company', '=', 1)],limit=1)
            colliding_partner = self.browse(colliding_partner.id)
            if colliding_partner and colliding_partner.company_id.id == partner.company_id.id:
                if colliding_partner.commercial_partner_id != partner.commercial_partner_id:
                    raise UserError(_('The VAT number [%s] for this partner is also registered with partner [%s] Each partner should have unique vat number.') % (colliding_partner[0].vat,colliding_partner[0].name))
            else:
                #TDE Fix false return should raise
                self.check_vat_tr(partner.vat)
        return super(ResPartner,self).check_vat()



    @api.multi
    def write(self,values):
        if 'vat' in values:
            if values['vat']:
                values['vat'] = re.sub(r'\W+', '', values['vat']).upper()
                #  self.check_vat()
        return super(ResPartner,self).write(values)
    
    @api.model
    def create(self,values):
        if 'vat' in values:
            if values['vat']:
                values['vat'] = re.sub(r'\W+', '', values['vat']).upper()
            #self.check_vat()
        return super(ResPartner,self).create(values)