from openerp import models, fields, api, _


class update_discount(models.TransientModel):
    _name = 'update.discount'

    @api.model
    def default_get(self, fields):
        res = super(update_discount, self).default_get(fields)
        context = dict(self._context)
        active_id = context.get('active_id')
        so_line_rec = self.env['sale.order.line'].browse(active_id)
        if so_line_rec.unit_discounted:
            res.update({'discount_price': so_line_rec.unit_discounted})
        return res

    discount_price = fields.Float('Discount Price')

    @api.multi
    def update_discount_price(self):
        context = dict(self._context)
        active_id = context.get('active_id')
        print ':::CCC', context
        so_line_rec = self.env['sale.order.line'].browse(active_id)
        print '::so_line_rec', so_line_rec, self.discount_price
        so_line_rec.write({'unit_discounted': self.discount_price})
        return True
