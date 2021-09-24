from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def action_view_mos(self):
        action = self.env.ref('mrp.mrp_production_report').read()[0]
        action['domain'] = [('product_tmpl_id', 'in', self.ids)]
        action['context'] = {
            'search_default_last_year_mo_order': 1,
            'search_default_status': 1, 'search_default_scheduled_month': 1,
            'graph_measure': 'product_uom_qty',
        }
        return action