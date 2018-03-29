# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import re

def clean_vals(vals):
    if 'vat' in vals:
        vals['vat'] = filter(unicode.isalnum, unicode(vals['vat']))
    
    if 'email' in vals:
        s = unicode(vals['email']).lower()
        s = re.sub(u'[ğ]','g',re.sub(u'[ç]','c',re.sub(u'[ş]','s',re.sub(u'[ı]','i',re.sub(u'[ü]','u',re.sub(u'[ö]','o',s))))))
        vals['email'] = s 
    
    return vals

class res_partner(osv.osv):
    _inherit = 'res.partner'

    def check_vat(self, cr, uid, ids, context=None):
        for partner in self.browse(cr, uid, ids, context=context):
            if partner.sanitized_vat == '11111111111' or partner.sanitized_vat == '2222222222' :
                continue
            if not partner.vat:
                continue
            if partner.parent_id:
                continue
            colliding_partner = self.search(cr, uid, [('sanitized_vat', '=', partner.sanitized_vat),('id', '!=', partner.id),('is_company', '=', 1)],limit=1, context=context)
            colliding_partner = self.browse(cr, uid, colliding_partner)
            if colliding_partner and colliding_partner.company_id.id == partner.company_id.id:
                if colliding_partner.commercial_partner_id != partner.commercial_partner_id:
                    return False
        return super(res_partner, self).check_vat(cr, uid, ids, context=context)

    def _construct_constraint_msg(self, cr, uid, ids, context=None):
        for partner in self.browse(cr, uid, ids, context=context):
            if not partner.vat:
                continue
            if partner.parent_id:
                continue
            colliding_partner = self.search(cr, uid, [('sanitized_vat', '=', partner.sanitized_vat),('id', '!=', partner.id),('is_company', '=', 1)],limit=1, context=context)
            colliding_partner = self.browse(cr, uid, colliding_partner)
            if colliding_partner and colliding_partner.company_id.id == partner.company_id.id:
                if colliding_partner.commercial_partner_id != partner.commercial_partner_id:
                    return '\n' + _('The VAT number [%s] for this partner is also registered with partner [%s] Each partner should have unique vat number.') % (colliding_partner[0].vat,colliding_partner[0].name)
            return '\n' + _('The VAT number [%s] for partner [%s] does not seem to be valid. ') % (partner.vat, partner.display_name)

    _constraints = [(check_vat, _construct_constraint_msg, ["vat"])]


    

    def write(self, cr, uid, ids, vals, context=None):
        vals = clean_vals(vals)
        return super(res_partner, self).write(cr, uid, ids, vals, context=context)

    def create(self, cr, uid, vals, context=None):
        vals = clean_vals(vals)
        return super(res_partner, self).create(cr, uid, vals, context=context)
