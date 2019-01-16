'''
Created on Jan 16, 2019

@author: Codequarters
'''
from odoo import models,fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    #altinkaya61
    x_comment_export = fields.Text('ihracaat fatura notu')
    z_tevkifatli_mi = fields.Boolean(';TEVKiFATLI', help="Eger fatura tevkifatli fatura ise bu alan secilmeli Sadece zirve programi transferinde kullanilmaktadir.")
