from openerp import models, fields, api, _


class update_discount(models.TransientModel):
    _name = 'update.discount'

    @api.model
    def default_get(self, fields):
        res = super(update_discount, self).default_get(fields)
        context = dict(self._context)
        active_id = context.get('active_id')
        so_line_rec = self.env['sale.order.line'].browse(active_id)
        if so_line_rec.discount_unit_price:
            res.update({'discount_price': so_line_rec.discount_unit_price})
        return res

    discount_price = fields.Float('Discount Price')

    @api.multi
    def update_discount_price(self):
        context = dict(self._context)
        active_id = context.get('active_id')
        so_line_rec = self.env['sale.order.line'].browse(active_id)
        so_line_rec.write({'discount_unit_price': self.discount_price})
        return True
