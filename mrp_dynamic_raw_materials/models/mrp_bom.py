# -*- encoding: utf-8 -*-
#
#Created on Mar 5, 2018
#
#@author: dogan
#

import time

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.tools import float_compare, float_is_zero
from openerp import api, models, fields, tools, _
from openerp.exceptions import Warning as UserError


class MepBoMTemplateLineRule(models.Model):
    _name= 'mrp.bom.template_line.rule'
    
    template_line_id = fields.Many2one('mrp.bom.template_line','BoM Template Line')
    attribute_id = fields.Many2one('product.attribute',string='Component Attribute', required=True)
    bom_attribute_id = fields.Many2one('product.attribute',string='Product Attribute', required=True)
    offset = fields.Float('Offset')
    coeff = fields.Float('Coefficient')
    precision = fields.Integer('Precision')
    
    
    @api.multi
    def compute_attribute_value(self, bom_attribute_value):
        self.ensure_one()
        
        attr_val_obj = self.env['product.attribute.value']
        attr_val = bom_attribute_value * self.coeff + self.offset
        
       # attr_val = '%*.f' % (self.precision, attr_val)
        attr_val_id = attr_val_obj.search([('attribute_id', '=', self.attribute_id.id),('numeric_value', '=', attr_val)], limit=1)
          
        return attr_val_id
        
    

class MrpBoMTemplateLine(models.Model):
    _name = 'mrp.bom.template_line'
    
    bom_id = fields.Many2one('mrp.bom',string='BoM',required=False, ondelete='cascade')
    product_tmpl_id = fields.Many2one('product.template',string='Product Template', required=True)
    product_id = fields.Many2one('product.product',string='Product', compute='_compute_product')
    type=fields.Selection([('normal', 'Normal'), ('phantom', 'Phantom')], 'BoM Line Type', required=True,
                help="Phantom: this product line will not appear in the raw materials of manufacturing orders,"
                     "it will be directly replaced by the raw materials of its own BoM, without triggering"
                     "an extra manufacturing order.", default='normal')
    
    date_start = fields.Date('Valid From', help="Validity of component. Keep empty if it's always valid.")
    date_stop = fields.Date('Valid Until', help="Validity of component. Keep empty if it's always valid.")
    routing_id = fields.Many2one('mrp.routing', 'Routing', help="The list of operations (list of work centers) to produce the finished product. The routing is mainly used to compute work center costs during operations and to plan future loads on work centers based on production planning.")
        
    product_rounding = fields.Float('Product Rounding', help="Rounding applied on the product quantity.")
    product_efficiency = fields.Float('Manufacturing Efficiency', required=True, help="A factor of 0.9 means a loss of 10% within the production process.", default=1.0)
    property_ids = fields.Many2many('mrp.property', string='Properties') #Not used

    attribute_value_ids = fields.Many2many('product.attribute.value', string='Variants', help="BOM Product Variants needed form apply this line.")
    #child_line_ids = fields.One2many("mrp.bom.line", string="BOM lines of the referred bom", compute='_get_child_bom_lines')
    
    
    bom_attribute_ids = fields.Many2many('product.attribute',string='BoM Product Attributes',compute='_compute_bom_attributes')
    attribute_ids = fields.Many2many('product.attribute',string='Attributes',compute='_compute_attributes')
    product_qty = fields.Float('Quantity')
    product_uom = fields.Many2one('product.uom',string='UoM')
    product_uos_qty = fields.Float('Product UOS Qty')
    product_uos = fields.Many2one('product.uom', 'Product UOS', help="Product UOS (Unit of Sale) is the unit of measurement for the invoicing and promotion of stock.")
        
    variant_rule_ids = fields.One2many('mrp.bom.template_line.rule','template_line_id', string='Variant Rules')
    
#     @api.multi
#     def _get_child_bom_lines(self):
#         """If the BOM line refers to a BOM, return the ids of the child BOM lines"""
#         bom_obj = self.env['mrp.bom']
#         res = {}
#         for bom_template_line in self:
#             bom_id = bom_obj._bom_find(
#                 product_tmpl_id=bom_template_line.product_tmpl_id.id,
#                 product_id=bom_template_line.product_id.id)
#             if bom_id:
#                 child_bom = bom_obj.browse(cr, uid, bom_id, context=context)
#                 res[bom_line.id] = [x.id for x in child_bom.bom_line_ids]
#             else:
#                 res[bom_line.id] = False
#         return res

    
    @api.multi
    def _compute_variant_values(self):
        self.ensure_one()
        bom_id = self.bom_id
        product_to_produce = self.env.context.get('product_produce', False) or \
                                 bom_id.product_id or \
                                 bom_id.product_tmpl_id.product_variant_ids[0]
        
        product_produce_values = { att_val.attribute_id.id:att_val.numeric_value for att_val in product_to_produce.attribute_value_ids }
        product_consume_values = self.env['product.attribute.value']
        
        for rule in self.variant_rule_ids:
            val = product_produce_values[rule.bom_attribute_id.id]
            variant_val = rule.compute_attribute_value(val)
            product_consume_values |= variant_val
        
        return product_consume_values
    
    @api.multi
    @api.depends('product_tmpl_id')
    def _compute_product(self):
        for bom_tmpl_line in self:
            val_ids = bom_tmpl_line._compute_variant_values()
            if len(val_ids) != len(bom_tmpl_line.variant_rule_ids):
                # one or more values are not defined in the values
                bom_tmpl_line.product_id = False
            
            else:
                def has_all_values(product):
                    return product.attribute_value_ids == val_ids

                variant_ids = bom_tmpl_line.product_tmpl_id.product_variant_ids.filtered(has_all_values)
            
                bom_tmpl_line.product_id = variant_ids and variant_ids[0] or False
                
            
                
    
    @api.multi
    @api.depends('product_tmpl_id')
    def _compute_attributes(self):
        for line in self:
            line.attribute_ids = line.product_tmpl_id.attribute_line_ids.mapped('attribute_id')
            
    @api.multi
    @api.depends('bom_id','bom_id.product_tmpl_id')
    def _compute_bom_attributes(self):
        for line in self:
            line.bom_attribute_ids = line.bom_id.product_tmpl_id.attribute_line_ids.mapped('attribute_id')
            
    @api.onchange('product_uom')  
    def onchange_uom(self):
        self.ensure_one()
        res = {'value': {}}
        if not self.product_uom:
            return res
        
        if self.product_uom.category_id.id != self.product_tmpl_id.uom_id.category_id.id:
            res['warning'] = {'title': _('Warning'), 'message': _('The Product Unit of Measure you chose has a different category than in the product form.')}
            res['value'].update({'product_uom': self.product_tmpl_id.uom_id.id})
        
        return res
       

class MrpBoM(models.Model):
    _inherit = 'mrp.bom'
    
    template_line_ids = fields.One2many('mrp.bom.template_line','bom_id', string='Template Lines')
    
    @api.model
    def _skip_template_line(self,  line, product):
        """ Control if a BoM template line should be produce, can be inherited for add
        custom control.
        @param line: BoM template line.
        @param product: Selected product produced.
        @return: True or False
        """
        if line.date_start and line.date_start > time.strftime(DEFAULT_SERVER_DATE_FORMAT) or \
            line.date_stop and line.date_stop < time.strftime(DEFAULT_SERVER_DATE_FORMAT):
                return True
        # all bom_line_id variant values must be in the product
        if line.attribute_value_ids:
            if not product or (set(map(int,line.attribute_value_ids or [])) - set(map(int,product.attribute_value_ids))):
                return True
        return False
    
    
    
    @api.model
    def _prepare_template_consume_line(self, tmpl_line, product_id, quantity, factor=1):
        uos_qty = (tmpl_line.product_uos and
                   self._factor(
                       tmpl_line.product_uos_qty * factor,
                       tmpl_line.product_efficiency, tmpl_line.product_rounding))
        return {
            'name': product_id.name,
            'product_id': product_id.id,
            'product_qty': quantity,
            'product_uom': tmpl_line.product_uom.id,
            'product_uos_qty': uos_qty or False,
            'product_uos': tmpl_line.product_uos.id,
        }
    
    @api.v7
    def _bom_explode(self, cr, uid, bom, product, factor, properties=None,
                     level=0, routing_id=False, previous_products=None,
                     master_bom=None, context=None):
        
        return super(MrpBoM, self)._bom_explode(cr, uid, bom,
            product, factor, properties=properties, level=level,
            routing_id=routing_id, previous_products=previous_products,
            master_bom=master_bom, context=context)
        
    
    @api.v8
    def _bom_explode(self, product, factor, properties=None, level=0,
                     routing_id=False, previous_products=None,
                     master_bom=None):
        result, result2 = super(MrpBoM, self)._bom_explode(product, factor, properties=properties, level=level,
                                                            routing_id=routing_id, previous_products=previous_products,
                                                            master_bom=master_bom)
        master_bom = master_bom or self
            
        uom_obj = self.env['product.uom']
        
        for tmpl_line in self.template_line_ids:
            if self._skip_template_line(tmpl_line, product):
                continue
            if (set(map(int, tmpl_line.property_ids or [])) -
                    set(properties or [])):
                continue
            product_tmpl_id = tmpl_line.product_tmpl_id.id
            if (previous_products and
                    product_tmpl_id in previous_products):
                raise UserError(
                    _('BoM "%s" contains a BoM line with a product recursion: '
                      '"%s".') % (master_bom.name,
                                  tmpl_line.product_tmpl_id.name_get()[0][1]))
            
            
            #TODO: find the matching product and explode
            product_id = tmpl_line.with_context(product_produce=product).product_id
            if not product_id:
                raise UserError('no product found for template %s' % tmpl_line.product_tmpl_id.display_name)
            
            quantity = self._factor(
                tmpl_line.product_qty * factor,
                tmpl_line.product_efficiency, tmpl_line.product_rounding)
            
            bom2 = self._bom_find(product_id=product_id.id, properties=properties)
            
            
            # If BoM should not behave like PhantoM, just add the product,
            # otherwise explode further
            if (tmpl_line.type != "phantom" and
                    (not bom2 or bom2.type != "phantom")):
                result.append(
                    self._prepare_template_consume_line(tmpl_line, product_id, quantity, factor))
            elif bom2:
                all_prod = [self.product_tmpl_id.id] + (previous_products or [])
                #bom2 = self.browse(bom_id)
                # We need to convert to units/UoM of chosen BoM
                factor2 = uom_obj._compute_qty(
                    tmpl_line.product_uom.id, quantity, bom2.product_uom.id)
                quantity2 = factor2 / bom2.product_qty
                res = bom2._bom_explode(
                    product_id, quantity2, properties=properties,
                    level=level + 10, previous_products=all_prod,
                    master_bom=master_bom)
                result = result + res[0]
                result2 = result2 + res[1]
            else:
                raise UserError(
                    _('BoM "%s" contains a phantom BoM line but the product '
                      '"%s" does not have any BoM defined.') %
                    (master_bom.name, product_id.name))
            
            
        return result, result2
    
    
    @api.multi
    def _find_matching_product(self):
        ''' Find the matching variant component for the rules
        '''
        self.ensure_one()
        return self.product_variant_ids[0]
        
        
    
class MrpBoMLine(models.Model):
    _inherit = 'mrp.bom.line'
    
    factor_attribute_id = fields.Many2one('product.attribute',string='Factor Attribute',
                                          help='End product attribute to use for raw material calculation')
    attribute_factor = fields.Float(string='Factor',help='Factor to multiply by the numeric value of attribute')
    
    