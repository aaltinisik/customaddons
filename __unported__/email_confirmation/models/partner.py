# -*- coding: utf-8 -*-



from odoo import models,fields,api
import re





class ResPartner(models.Model):
    _inherit="res.partner"
    
    
    
    
    def clean_vals(self,vals):
        if 'email' in vals:
            if vals['email']:
                s = vals['email'].lower()
                s = re.sub(u'[ğ]','g',re.sub(u'[ç]','c',re.sub(u'[ş]','s',re.sub(u'[ı]','i',re.sub(u'[ü]','u',re.sub(u'[ö]','o',s))))))
                vals['email'] = s
    
    
    
    
    
    @api.multi
    def write(self,values):
        self.clean_vals(values)
        return super(ResPartner,self).write(values)
    
    @api.model
    def create(self,values):
        self.clean_vals(values)
        return super(ResPartner,self).create(values)
    
    
    