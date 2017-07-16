from openerp import fields, models, api

class stock_package(models.Model):
    _inherit = "stock.quant.package"
    
    width = fields.Float('Width')
    length = fields.Float('Length')
    height = fields.Float('Height')
    net_weight = fields.Float('Net Weight')
    gross_weight = fields.Float('Gross Weight')


    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = record.name + '(' + str(record.width) + ' x ' + str(record.length) + ' x ' + str(record.height) + ' cm  Net: ' + str(record.net_weight) + ' Kg Gross: ' + str(record.gross_weight) + 'Kg' + ')'
            res.append((record.id, name))
        return res

    @api.onchange('ul_id')
    def onchange_ul_id(self):
      if self.ul_id:
        self.width = self.ul_id.width
        self.height = self.ul_id.height
        self.length = self.ul_id.length