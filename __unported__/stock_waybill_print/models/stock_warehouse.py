from odoo import models, fields, api


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    waybill_sequence_id = fields.Many2one('ir.sequence',
                                          domain="[('company_id', '=', company_id), ('code', '=', 'stock.waybill.print')]",
                                          string='Waybill Sequence')
    waybill_printer = fields.Many2one(
       'printing.printer',
       string=u'İrsaliye Yazıcısı',
       help="",
       required=False,
       company_dependent=True)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # document_number = fields.Char(string='İrsaliye Numarası', help='Basılı irsaliye numarası')
    document_page_count = fields.Integer('Page Count', compute='_compute_page_count')

    @api.one
    def _compute_page_count(self):
        if len(self.move_lines) % 24 != 0:
            self.document_page_count = int(len(self.move_lines) / 24) + 1
        else:
            self.document_page_count = len(self.move_lines) / 24

    @api.multi
    def action_print(self):
        return {}
