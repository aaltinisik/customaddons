# -*- encoding: utf-8 -*-
#
#Created on Jan 20, 2020
#
#@author: dogan
#
from odoo import models,fields,api


class MigrationMapping(models.AbstractModel):
    _name = "migration.mapping"
    
    v8_id = fields.Integer(string="V8 ID",store=True)


    
class Rescountry(models.Model):
    _name = 'res.country'
    _inherit= ["res.country",'migration.mapping'] 
    
class RescountryState(models.Model):
    _name = 'res.country.state'
    _inherit= ["res.country.state",'migration.mapping']

class AddressDistrict(models.Model):
    _name = 'address.district'
    _inherit= ["address.district",'migration.mapping']

class AddressRegion(models.Model):
    _name = 'address.region'
    _inherit= ["address.region",'migration.mapping']

class AddressNeighbour(models.Model):
    _name = 'address.neighbour'
    _inherit= ["address.neighbour",'migration.mapping']

class ResPartner(models.Model):
    _name="res.partner"
    _inherit = ['res.partner','migration.mapping']


class ResPartnerCategory(models.Model):
    _name="res.partner.category"
    _inherit = ['res.partner.category','migration.mapping']    
    
class AccountPaymentTerm(models.Model):
    _name = "account.payment.term"
    _inherit=["account.payment.term",'migration.mapping']
    

class ResBartnerBank(models.Model):
    _name="res.partner.bank"
    _inherit=["res.partner.bank","migration.mapping"]


class ProductPricelist(models.Model):
    _name="product.pricelist"
    _inherit=["product.pricelist",'migration.mapping']

class ProductCategory(models.Model):
    _name="product.category"
    _inherit=["product.category","migration.mapping"]

class UomCategory(models.Model):
    _name="uom.category"
    _inherit=['uom.category',"migration.mapping"]

class UomUom(models.Model):
    _name="uom.uom" 
    _inherit=['uom.uom',"migration.mapping"]   
    
class ProductAttribute(models.Model):
    _name="product.attribute"
    _inherit=['product.attribute','migration.mapping']
    
class ProductAttributeValue(models.Model):
    _name="product.attribute.value"
    _inherit=['product.attribute.value','migration.mapping']
    
class ProductTemplateAttributeLine(models.Model):
    _name="product.template.attribute.line"
    _inherit=['product.template.attribute.line','migration.mapping']
    
class ProductTemplateAttributeValue(models.Model):
    _name="product.template.attribute.value"
    _inherit=['product.template.attribute.value','migration.mapping']                
    
class ProductTemplate(models.Model):
    _name="product.template"
    _inherit = ['product.template','migration.mapping']
    
class ProductProduct(models.Model):
    _name="product.product"
    _inherit=['product.product','migration.mapping']        

class DeliveryCarrier(models.Model):
    _name = 'delivery.carrier'
    _inherit =["delivery.carrier","migration.mapping"]

class AccountTax(models.Model):
    _name="account.tax"
    _inherit=["account.tax","migration.mapping"]



    
    
    