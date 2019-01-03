# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields


class account_invoice(osv.Model):
    _inherit = 'account.invoice'
    _columns = {
         'x_comment_export': fields.text('ihracaat fatura notu'),
         'z_tevkifatli_mi': fields.boolean(';TEVKiFATLI', help="Eger fatura tevkifatli fatura ise bu alan secilmeli Sadece zirve programi transferinde kullanilmaktadir.")
		 }
