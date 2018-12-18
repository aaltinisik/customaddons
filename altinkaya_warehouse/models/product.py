
from openerp import models, fields, api, _



class product_putaway_strategy(models.Model):
    _inherit = 'product.putaway'
  
    @api.model
    def _get_putaway_options(self):
        ret = super(product_putaway_strategy, self)._get_putaway_options()
        return ret + [('fixed_all','Fixed for all products')]

    method = fields.Selection(
        selection=_get_putaway_options,
        string="Method",
        required=True)
    
    fixed_all_location_id = fields.Many2one('stock.location',string='Fixed Location for all products')

    @api.onchange('method')
    def onchange_method(self):
        if self.method != 'fixed_all':
            self.fixed_all_location_id = False
        
    @api.model
    def putaway_apply(self,putaway_strat, product):
        if putaway_strat.method == 'fixed_all':
            return putaway_strat.fixed_all_location_id.id
        else:
            return super(product_putaway_strategy, self).putaway_apply(putaway_strat, product)


class product_product(models.Model):
    _inherit = "product.product"

    qty_available_sincan = fields.Float('Sincan Depo Mevcut',compute='_compute_custom_available',search='_search_qty_custom')
    qty_available_merkez = fields.Float('Merkez Depo Mevcut',compute='_compute_custom_available')
    qty_incoming_sincan = fields.Float('Sincan Depo Gelen',compute='_compute_custom_available')
    qty_incoming_merkez = fields.Float('Merkez Depo Gelen',compute='_compute_custom_available')
    qty_outgoing_sincan = fields.Float('Sincan Depo Giden',compute='_compute_custom_available')
    qty_outgoing_merkez = fields.Float('Merkez Depo Giden',compute='_compute_custom_available')
    qty_virtual_sincan = fields.Float('Sincan Depo Tahmini',compute='_compute_custom_available')
    qty_virtual_merkez = fields.Float('Merkez Depo Tahmini',compute='_compute_custom_available')
    
    
#    type_variant = fields.Selection([('product','Stockable Product'),('consu','Consumable'),('service','Service')], string="Product Type", default=False,store=True)
#    type = fields.Selection([('product','Stockable Product'),('consu','Consumable'),('service','Service')],compute='_compute_type')
    
    
#    @api.multi
#    def _compute_type(self):
#        for product in self:
#            product.type = product.type_variant or product.product_tmpl_id.type
            
    
    def _search_qty_custom(self, operator, value):
        return [('id', 'in', self.with_context({'location':28})._search_qty_available(operator, value))]
                 
    
    @api.multi
    def _compute_custom_available(self):
        for product in self:
            product.qty_available_sincan = product.with_context({'location':28}).qty_available
            product.qty_available_merkez = product.with_context({'location':10}).qty_available
            product.qty_incoming_sincan = product.with_context({'location':28}).incoming_qty
            product.qty_incoming_merkez = product.with_context({'location':10}).incoming_qty
            product.qty_outgoing_sincan = product.with_context({'location':28}).outgoing_qty
            product.qty_outgoing_merkez = product.with_context({'location':10}).outgoing_qty
            product.qty_virtual_sincan = product.with_context({'location':28}).virtual_available
            product.qty_virtual_merkez = product.with_context({'location':10}).virtual_available
