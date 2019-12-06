'''
Created on Jan 16, 2019

@author: cq
'''

from odoo import models,fields





class ResUsers(models.Model):
    _inherit = 'res.users'
    
    default_procurement_wh_id = fields.Many2one('stock.warehouse',string='Default Procurement Warehouse')


class ResCompany(models.Model):
    _inherit='res.company'
    
    
    hash_code = fields.Char('Hash Comm Code', size=200, help="Used in comm with ext services")
        



class ResPartner(models.Model):
    _inherit = "res.partner"

    z_old_tel = fields.Char('Eski Tel', size=64, required=False)
    z_old_fax = fields.Char('Eski Faks', size=64, required=False)
    z_old_cep = fields.Char('Eski Cep', size=64, required=False)
    z_contact_name = fields.Char('ilgili kişi', size=64, required=False)
    z_tel_kampanya = fields.Boolean('Kampanyalarda Aranmayacak',default=False, help=u"Seçili ise telefon kampanyalarında aranmayacak.")
    z_kamp_2016A = fields.Boolean('2016 Katalog için arandı', help=u"2016 Temmuz Katalog gönderme kampanyası icin arandi.")
    z_kamp_2017A = fields.Boolean('2017 Adres güncelleme için arandı', help=u"2017 Temmuz Adres günceleme için arandı.")
    z_kat_postala = fields.Boolean('Katalog Postala', help=u"Katalog Posta ile gönderilecek.")
    z_kat_postalandi = fields.Boolean('Katalog Postalandi', help=u"Katalog Posta ile gönderildi.")
    z_kat_email = fields.Boolean('Katalog E-mail', help=u"Katalog email ile gönderilecek.")

    
    #altinkaya61
    z_muhasebe_kodu = fields.Char('Zirve Muhasebe kodu', size=64, required=False, translate=False)
    
    #altinkaya
    
    x_vergidairesi = fields.Char('Vergi Dairesi', size=64)
    x_vergino = fields.Char('Vergi No', size=64)
    devir_yapildi = fields.Boolean('Devir yapıldı')