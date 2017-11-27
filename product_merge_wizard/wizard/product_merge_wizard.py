'''
Created on Nov 27, 2017

@author: dogan
'''


from openerp import models, fields, api
from openerp.tools.translate import _
from openerp import exceptions

class ProductMergeWizard(models.TransientModel):
    _name = 'product.merge.wizard'
    
    name = fields.Char('Product Name', required=True)
    attribute_line_ids = fields.One2many('product.merge.wizard.attribute_line','wizard_id',string='Attributes')
    product_line_ids = fields.One2many('product.merge.wizard.product_line','wizard_id',string='Products')
    attribute_value_ids = fields.Many2many('product.attribute.value','Attribute Value IDs',compute='_compute_attribute_ids')
    
    
        
       
       
    @api.one
    @api.depends('attribute_line_ids.value_ids')
    def _compute_attribute_ids(self):
        self.attribute_value_ids = self.attribute_line_ids.mapped('value_ids')
    
    
    @api.multi
    def action_merge(self):
        self.ensure_one()
        
        attribute_ids = {}
        for line in self.attribute_line_ids:
            if attribute_ids.get(line.attribute_id.id,False):
                raise exceptions.ValidationError(_('You can not add an attribute mode than once'))
        
            attribute_ids.update({line.attribute_id.id:True})
            
        
        vals = {'create_product_product':False,
                'attribute_line_ids':[(6,False,{'attribute_id': al.attribute_id.id, 
                                                'value_ids':al.value_ids}) for al in self.attribute_line_ids]}
        
        product_tmpl_id = self.env['product.template'].with_context(vals).create({'name':self.name})
        
        for product_line in self.product_line_ids:
            product_line.product_id.attribute_value_ids = product_line.value_ids
        
        self.mapped('product_line_ids.product_id').write({'product_tmpl_id':product_tmpl_id.id})
        
        
        return {
            'name': _('Product'),
            'view_type':'form',
            'view_mode':'tree,form',
            'res_model':'product.template',
            'view_id':False,
            'type':'ir.actions.act_window',
            'domain':[('id','=',product_tmpl_id.id)],
            'context':self.env.context,
        }
    

class ProductMergeAttributeLine(models.TransientModel):
    _name = 'product.merge.wizard.attribute_line'
    
    wizard_id = fields.Many2one('product.merge.wizard',string='Wizard')
    attribute_id = fields.Many2one('product.attribute',string='Attribute')
    required = fields.Boolean('Required')
    value_ids = fields.Many2many('product.attribute.value',relation='product_merge_attr_val_rel',string='Values', domain="[('attribute_id','=',attribute_id)]")
    
class ProductMergeProductLine(models.TransientModel):
    _name = 'product.merge.wizard.product_line'
    
    wizard_id = fields.Many2one('product.merge.wizard',string='Wizard')
    product_id = fields.Many2one('product.product',string='Product')
    value_ids = fields.Many2many('product.attribute.value',relation='product_merge_product_att_val_rel')
    
    