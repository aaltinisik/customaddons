# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields


class res_partner(osv.Model):
    _inherit = 'res.partner'
    _columns = {
         'z_muhasebe_kodu': fields.char('Zirve Muhasebe kodu', size=64, required=False, translate=False)
    }
