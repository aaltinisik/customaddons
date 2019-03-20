



from odoo import models,fields,api




class DeliveryCarrier(models.Model):
    _inherit='delivery.carrier'
    
    
    partner_id =fields.Many2one('res.partner','Carrier')