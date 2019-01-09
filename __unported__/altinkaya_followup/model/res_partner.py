from openerp.osv import orm, osv, fields


class res_partner(orm.Model):
    _inherit = ['res.partner', 'phone.common']
    _name = 'res.partner'

    def create(self, cr, uid, vals, context=None):
        vals_reformated = self._generic_reformat_phonenumbers(
            cr, uid,None, vals, context=context)
        return super(res_partner, self).create(
            cr, uid, vals_reformated, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        vals_reformated = self._generic_reformat_phonenumbers(
            cr, uid,None,vals, context=context)
        return super(res_partner, self).write(
            cr, uid, ids, vals_reformated, context=context)


    def _followup_faxno(self, cr, uid, ids, name, args, context=None):
        res = {}
        for partner in self.browse(cr, uid, ids, context=context):
            res[partner.id] = self._show_followup_faxno(cr, uid, partner, context=context)
        return res

    def _followup_faxaddres(self, cr, uid, ids, name, args, context=None):
        res = {}
        for partner in self.browse(cr, uid, ids, context=context):
            res[partner.id] = self._show_followup_faxaddres(cr, uid, partner, context=context)
        return res

    def _followup_emailaddres(self, cr, uid, ids, name, args, context=None):
        res = {}
        for partner in self.browse(cr, uid, ids, context=context):
            res[partner.id] = self._show_followup_emailaddres(cr, uid, partner, context=context)
        return res

    def _show_followup_faxno(self, cr, uid, partner, without_company=False, context=None):

        '''
        To show followup fax no if empty show partner fax

        :param partner: browse record of the res.partner
        :returns: show followup fax no if empty show partner fax
        :rtype: string
        '''
        if partner.followup_use_fax:
            if partner.followup_fax:
                return partner.followup_fax
            else:
                return partner.fax
        else:
            return ""

    def _show_followup_faxaddres(self, cr, uid, partner, without_company=False, context=None):

        '''
        To show followup fax no if empty show partner fax

        :param partner: browse record of the res.partner
        :returns: show followup fax no if empty show partner fax
        :rtype: string
        '''
        if partner.followup_use_fax and partner.fax:
            if partner.followup_fax:
                return partner.followup_fax + "@fax.tc"
            else:
                return partner.fax + "@fax.tc"
        else:
            return ""

    def _show_followup_emailaddres(self, cr, uid, partner, without_company=False, context=None):

        '''
        To show followup email if empty show partner email

        :param partner: browse record of the res.partner
        :returns: show followup email no if empty show partner email
        :rtype: string
        '''
        if partner.followup_use_email:
            if partner.followup_email:
                return partner.followup_email
            else:
                return partner.email
        else:
            return ""


    _columns = {

    'followup_email': fields.char('Follow up Email', size=240),
    'followup_use_email': fields.boolean('Use Email in followup'),
    'followup_fax': fields.char('Follow up Fax', size=64),
    'followup_use_fax': fields.boolean('Use Fax in followup'),
    'followup_phone': fields.char('Follow up Phone', size=64),
    'followup_mobile': fields.char('Follow up Mobile', size=64),
    'followup_name': fields.char('Payment Responsible', size=100),
    'followup_note': fields.char('Follow up note', size=200),
    'followup_faxno': fields.function(_followup_faxno,  type='char', string='Fax No to use in followups'),
    'followup_faxaddres': fields.function(_followup_faxaddres,  type='char', string='Fax email address to use in followups'),
    'followup_emailaddres': fields.function(_followup_emailaddres,  type='char', string='Email address to use in followups'),

    }

    _defaults = {
        'followup_use_email': 1,
        'followup_use_fax': 1,
        'vat_subjected': 1,
    }


res_partner()

