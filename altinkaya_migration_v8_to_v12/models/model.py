# -*- encoding: utf-8 -*-
#
#Created on Jan 20, 2020
#
#@author: dogan
#
from odoo import models,fields,api


class MigrationMapping(models.AbstractModel):
    _name = "migration.mapping"
    _description = "Base model for v8 to v12 migration"
    v8_id = fields.Integer(string="V8 ID",store=True, readonly=True)


    
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


class StockLocation(models.Model):
    _name="stock.location"
    _inherit = ['stock.location',"migration.mapping"]
    
class StockLocationRoute(models.Model):
    _name="stock.location.route"
    _inherit = ['stock.location.route',"migration.mapping"]    
    
class ProductPriceType(models.Model):
    _name="product.price.type"
    _inherit = ['product.price.type',"migration.mapping"]   
    
class ProductPricelistItem(models.Model):
    _name="product.pricelist.item"
    _inherit = ['product.pricelist.item',"migration.mapping"]

class PartnerWorksector(models.Model):
    _name="partner.worksector"
    _inherit=['partner.worksector',"migration.mapping"]     

class StockQuant(models.Model):
    _name="stock.quant"
    _inherit=['stock.quant',"migration.mapping"]

class StockRule(models.Model):
    _name="stock.rule"
    _inherit = ["stock.rule","migration.mapping"]

    
class StockWarehouse(models.Model):
    _name="stock.warehouse"
    _inherit = ["stock.warehouse","migration.mapping"]

class StockWarehouseOrderpoint(models.Model):
    _name="stock.warehouse.orderpoint"
    _inherit = ["stock.warehouse.orderpoint","migration.mapping"]
    
class MrpWorkcenter(models.Model):
    _name="mrp.workcenter"
    _inherit = ['mrp.workcenter',"migration.mapping"]     
    
class MrpBom(models.Model):
    _name="mrp.bom"
    _inherit = ["mrp.bom","migration.mapping"]

class MrpBomWcparameter(models.Model):
    _name="mrp.bom.wcparameter"
    _inherit = ["mrp.bom.wcparameter","migration.mapping"]    
        
class CrmTeam(models.Model):
    _name="crm.team"     
    _inherit=["crm.team","migration.mapping"]  
    
class SaleOrder(models.Model):
    _name="sale.order"
    _inherit=["sale.order","migration.mapping"]

class SaleOrderLine(models.Model):
    _name="sale.order.line"
    _inherit=["sale.order.line","migration.mapping"]


class AccountInvoice(models.Model):
    _name="account.invoice"
    _inherit=["account.invoice","migration.mapping"]    
        
class AccountInvoiceLine(models.Model):
    _name="account.invoice.line"
    _inherit=["account.invoice.line","migration.mapping"]     
    
    
class AccountEinvoiceProvider(models.Model):
    _name="account.einvoice.provider"
    _inherit =["account.einvoice.provider","migration.mapping"]   
     
class AccountEinvoiceSender(models.Model):
    _name="account.einvoice.sender"
    _inherit=["account.einvoice.sender","migration.mapping"]      
          
  
class AccountEinvoicePostbox(models.Model):
    _name="account.einvoice.postbox"
    _inherit=["account.einvoice.postbox","migration.mapping"]
      
class AccountJournal(models.Model):
    _name="account.journal"
    _inherit=["account.journal","migration.mapping"]    

class AccountAccount(models.Model):
    _name="account.account"
    _inherit=["account.account","migration.mapping"]    

class AccountGroup(models.Model):
    _name="account.group"
    _inherit=["account.group","migration.mapping"]  
    
class StockPicking(models.Model):
    _name="stock.picking"
    _inherit=["stock.picking","migration.mapping"]
        
class StockMove(models.Model):
    _name="stock.move"
    _inherit=["stock.move","migration.mapping"]    

class AccountMove(models.Model):
    _name="account.move"
    _inherit=["account.move","migration.mapping"]    


class AccountMoveLine(models.Model):
    _name="account.move.line"
    _inherit=["account.move.line","migration.mapping"]    
    
class HrEmployee(models.Model):
    _name="hr.employee"
    _inherit=["hr.employee","migration.mapping"]    
 
class MrpProduction(models.Model):
    _name="mrp.production"
    _inherit = ["mrp.production","migration.mapping"] 
 
class MrpWorkorder(models.Model):
    _name="mrp.workorder"
    _inherit = ["mrp.workorder","migration.mapping"] 
    
    