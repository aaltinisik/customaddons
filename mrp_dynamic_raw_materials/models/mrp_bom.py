# -*- encoding: utf-8 -*-
#
#Created on Mar 5, 2018
#
#@author: dogan
#
from openerp import api, models, fields, tools, _
from openerp.exceptions import Warning as UserError


class MrpBoM(models.Model):
    _inherit = 'mrp.bom'
    
    @api.v7
    def _bom_explode(self, cr, uid, bom, product, factor, properties=None,
                     level=0, routing_id=False, previous_products=None,
                     master_bom=None, context=None):
        """ Finds Products and Work Centers for related BoM for manufacturing
        order.

        Verbatim copy of core method extracting the hooks already merged on
        v9 branch.

        @param bom: BoM of particular product template.
        @param product: Select a particular variant of the BoM. If False use
        BoM without variants.
        @param factor: Factor represents the quantity, but in UoM of the BoM,
        taking into account the numbers produced by the BoM
        @param properties: A List of properties Ids.
        @param level: Depth level to find BoM lines starts from 10.
        @param previous_products: List of product previously use by bom
        explore to avoid recursion
        @param master_bom: When recursion, used to display the name of the
        master bom
        @return: result: List of dictionaries containing product details.
                 result2: List of dictionaries containing Work Center details.
        """
        return bom._bom_explode(
            product, factor, properties=properties, level=level,
            routing_id=routing_id, previous_products=previous_products,
            master_bom=master_bom)
        
    
    @api.v8
    def _bom_explode(self, product, factor, properties=None, level=0,
                     routing_id=False, previous_products=None,
                     master_bom=None):
        self.ensure_one()
        bom = self
        uom_obj = self.env["product.uom"]
        routing_obj = self.env['mrp.routing']
        master_bom = master_bom or bom
        factor = self._factor(
            factor, bom.product_efficiency, bom.product_rounding)
        result = []
        result2 = []
        routing = ((routing_id and routing_obj.browse(routing_id)) or
                   bom.routing_id or False)
        if routing:
            for wc_use in routing.workcenter_lines:
                result2.append(self._prepare_wc_line(
                    wc_use, level=level, factor=factor))
        for bom_line_id in bom.bom_line_ids:
            if self._skip_bom_line(bom_line_id, product):
                continue
            if (set(map(int, bom_line_id.property_ids or [])) -
                    set(properties or [])):
                continue
            product_tmpl_id = bom_line_id.product_id.product_tmpl_id.id
            if (previous_products and
                    product_tmpl_id in previous_products):
                raise UserError(
                    _('BoM "%s" contains a BoM line with a product recursion: '
                      '"%s".') % (master_bom.name,
                                  bom_line_id.product_id.name_get()[0][1]))
             
            qty_extra = 0.0
            if bom_line_id.factor_attribute_id:
                attribute_value_ids = product.attribute_value_ids
                attribute_value_id = attribute_value_ids.filtered(lambda v: v.attribute_id.id == bom_line_id.factor_attribute_id.id)
                if attribute_value_id:
                    qty_extra = (attribute_value_id.numeric_value * bom_line_id.attribute_factor)
             
             
            quantity = self._factor(
                (bom_line_id.product_qty + qty_extra) * factor,
                bom_line_id.product_efficiency, bom_line_id.product_rounding)
            bom_id = self._bom_find_prepare(bom_line_id, properties=properties)
            # If BoM should not behave like PhantoM, just add the product,
            # otherwise explode further
            if (bom_line_id.type != "phantom" and
                    (not bom_id or self.browse(bom_id).type != "phantom")):
                result.append(
                    self._prepare_consume_line(bom_line_id, quantity, factor))
            elif bom_id:
                all_prod = [bom.product_tmpl_id.id] + (previous_products or [])
                bom2 = self.browse(bom_id)
                # We need to convert to units/UoM of chosen BoM
                factor2 = uom_obj._compute_qty(
                    bom_line_id.product_uom.id, quantity, bom2.product_uom.id)
                quantity2 = factor2 / bom2.product_qty
                res = bom2._bom_explode(
                    bom_line_id.product_id, quantity2, properties=properties,
                    level=level + 10, previous_products=all_prod,
                    master_bom=master_bom)
                result = result + res[0]
                result2 = result2 + res[1]
            else:
                raise UserError(
                    _('BoM "%s" contains a phantom BoM line but the product '
                      '"%s" does not have any BoM defined.') %
                    (master_bom.name, self._get_bom_product_name(bom_line_id)))
        return result, result2
        
        
    
class MrpBoMLine(models.Model):
    _inherit = 'mrp.bom.line'
    
    factor_attribute_id = fields.Many2one('product.attribute',string='Factor Attribute',
                                          help='End product attribute to use for raw material calculation')
    attribute_factor = fields.Float(string='Factor',help='Factor to multiply by the numeric value of attribute')
    
    