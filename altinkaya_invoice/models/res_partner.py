from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    z_muhasebe_kodu = fields.Char('Zirve Muhasebe kodu', size=64, required=False, translate=False)
    z_receivable_export = fields.Char('Receivable Export', size=64, required=False)
    z_payable_export = fields.Char('Payable Export', size=64, required=False)
    purchase_default_account_id = fields.Many2one('account.account', string='Purchase Default Account', required=False,
                                                  help=u"Satın alma işlemlerinde varsayılan muhasebe hesabı.")
    accounting_contact = fields.Many2one('res.partner', string='Accounting Contact', required=False)

    @api.model
    def create(self, vals):
        if not vals.get('ref') and self._needsRef(vals=vals):
            vals['ref'] = self._get_next_ref(vals=vals)
            if vals['ref'] and vals['customer'] or vals['supplier']:
                country_id = self.env['res.country'].browse(vals['country_id'])
                if country_id and country_id.code != 'TR':
                    z_receivable_export = '120.Y%s' % (vals['ref'].strip() or '')
                    z_payable_export = '320.Y%s' % (vals['ref'].strip() or '')
                else:
                    z_receivable_export = '120.%s' % (vals['ref'].strip() or '')
                    z_payable_export = '320.%s' % (vals['ref'].strip() or '')
                vals.update({
                    'ref': vals['ref'],
                    'z_receivable_export': z_receivable_export,
                    'z_payable_export': z_payable_export
                })
        return super(ResPartner, self).create(vals)
