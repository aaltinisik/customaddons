


from odoo import models,fields




class MrpProduction(models.Model):
    _inherit='mrp.production'
    
    
    
    date_planned = fields.Datetime('Scheduled Date')
    date_start2 = fields.Datetime('Start Date')
    date_finished2 = fields.Datetime('End Date')
    priority = fields.Selection([('0','Not urgent'),('1','Normal'),('2','Urgent'),('3','Very Urgent')], 'Priority')