from openerp.osv import fields, osv
from openerp.tools.translate import _

class res_partner(osv.osv):
    _inherit = 'res.partner'

    def check_vat(self, cr, uid, ids, context=None):
        for partner in self.browse(cr, uid, ids, context=context):
            if partner.sanitized_vat == '11111111111':
                continue
            if not partner.vat:
                continue
            colliding_partner = self.search(cr, uid, [('sanitized_vat', '=', partner.sanitized_vat),('id', '!=', partner.id)],limit=1, context=context)
            colliding_partner = self.browse(cr, uid, colliding_partner)
            if colliding_partner and colliding_partner.company_id.id == partner.company_id.id:
                return False
        return super(res_partner, self).check_vat(cr, uid, ids, context=context)

    def _construct_constraint_msg(self, cr, uid, ids, context=None):
        for partner in self.browse(cr, uid, ids, context=context):
            if not partner.vat:
                continue
            colliding_partner = self.search(cr, uid, [('sanitized_vat', '=', partner.sanitized_vat),('id', '!=', partner.id)],limit=1, context=context)
            colliding_partner = self.browse(cr, uid, colliding_partner)
            if colliding_partner and colliding_partner.company_id.id == partner.company_id.id:
                return '\n' + _('The VAT number [%s] for this partner is also registered with partner [%s] Each partner should have unique vat number.') % (colliding_partner[0].vat,colliding_partner[0].name)
            return '\n' + _('The VAT number [%s] for partner [%s] does not seem to be valid. ') % (partner.vat, partner.name)

    _constraints = [(check_vat, _construct_constraint_msg, ["vat"])]