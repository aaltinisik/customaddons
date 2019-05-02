
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

    qty_available_sincan = fields.Float('Sincan Depo Mevcut',compute='_compute_custom_available', search='_search_qty_sincan')
    qty_available_merkez = fields.Float('Merkez Depo Mevcut',compute='_compute_custom_available', search='_search_qty_merkez')
    qty_available_enjek = fields.Float('Enjeksiyon Depo Mevcut',compute='_compute_custom2_available', search='_search_qty_enjek')
    qty_available_montaj = fields.Float('Montaj Depo Mevcut',compute='_compute_custom2_available', search='_search_qty_montaj')
    qty_available_cnc = fields.Float('CNC Depo Mevcut', compute='_compute_custom2_available',
                                        search='_search_qty_cnc')
    qty_available_metal = fields.Float('Metal Depo Mevcut', compute='_compute_custom2_available',
                                        search='_search_qty_metal')
    qty_available_boya = fields.Float('Boya Depo Mevcut', compute='_compute_custom2_available',
                                       search='_search_qty_boya')

    qty_incoming_sincan = fields.Float('Sincan Depo Gelen',compute='_compute_custom_available')
    qty_incoming_merkez = fields.Float('Merkez Depo Gelen',compute='_compute_custom_available')
    qty_outgoing_sincan = fields.Float('Sincan Depo Giden',compute='_compute_custom_available')
    qty_outgoing_merkez = fields.Float('Merkez Depo Giden',compute='_compute_custom_available')
    qty_virtual_sincan = fields.Float('Sincan Depo Tahmini',compute='_compute_custom_available')
    qty_virtual_merkez = fields.Float('Merkez Depo Tahmini',compute='_compute_custom_available')


    active_bom =  fields.Many2one('mrp.bom', string='Active Bom',
        compute='_find_active_bom', readonly=True, store=False)

    routing_id = fields.Many2one('mrp.routing', string='Rota',
        related='active_bom.routing_id',readonly=True)

    @api.one
    def _find_active_bom(self):
        self.active_bom = self.pool.get('mrp.bom')._bom_find(self._cr, self._uid, product_id=self.id,
                                                             product_tmpl_id=self.product_tmpl_id.id)

    
#    type_variant = fields.Selection([('product','Stockable Product'),('consu','Consumable'),('service','Service')], string="Product Type", default=False,store=True)
#    type = fields.Selection([('product','Stockable Product'),('consu','Consumable'),('service','Service')],compute='_compute_type')
    
    
#    @api.multi
#    def _compute_type(self):
#        for product in self:
#            product.type = product.type_variant or product.product_tmpl_id.type
            
    
    def _search_qty_merkez(self, operator, value):
        return [('id', 'in', self.with_context({'location':10})._search_qty_available(operator, value))]
                 
    def _search_qty_sincan(self, operator, value):
        return [('id', 'in', self.with_context({'location':28})._search_qty_available(operator, value))]

    def _search_qty_enjek(self, operator, value):
        return [('id', 'in', self.with_context({'location':34})._search_qty_available(operator, value))]

    def _search_qty_montaj(self, operator, value):
        return [('id', 'in', self.with_context({'location':80})._search_qty_available(operator, value))]

    def _search_qty_cnc(self, operator, value):
        return [('id', 'in', self.with_context({'location':9029})._search_qty_available(operator, value))]

    def _search_qty_boya(self, operator, value):
        return [('id', 'in', self.with_context({'location':71})._search_qty_available(operator, value))]

    def _search_qty_metal(self, operator, value):
        return [('id', 'in', self.with_context({'location':65})._search_qty_available(operator, value))]


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

    @api.multi
    def _compute_custom2_available(self):
        for product in self:
            product.qty_available_montaj = product.with_context({'location':80}).qty_available
            product.qty_available_enjek = product.with_context({'location':34}).qty_available
            product.qty_available_cnc = product.with_context({'location':9029}).qty_available
            product.qty_available_boya = product.with_context({'location':71}).qty_available
            product.qty_available_metal = product.with_context({'location':65}).qty_available
            
            
            
    
    


class mrpProduction(models.Model):
    _inherit = "mrp.production"

    qty_available_sincan = fields.Float('Sincan Depo Mevcut', related='product_id.qty_available_sincan')
    qty_available_merkez = fields.Float('Merkez Depo Mevcut', related='product_id.qty_available_merkez')
    qty_available_enjek = fields.Float('Enjeksiyon Depo Mevcut', related='product_id.qty_available_enjek')
    qty_available_montaj = fields.Float('Montaj Depo Mevcut', related='product_id.qty_available_montaj')
    qty_available_cnc = fields.Float('CNC Depo Mevcut', related='product_id.qty_available_cnc')
    qty_available_metal = fields.Float('Metal Depo Mevcut', related='product_id.qty_available_metal')
    qty_available_boya = fields.Float('Boya Depo Mevcut',related='product_id.qty_available_boya')
