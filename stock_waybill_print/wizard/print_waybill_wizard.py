# -*- encoding: utf-8 -*-


from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import Warning

class PrintWaybillWizard(models.TransientModel):
    _name = 'stock_waybill_print.print_waybill_wizard'
    
    
    @api.model
    def default_warehouse(self):
        picking_ids = self.env['stock.picking'].browse(self._context.get('active_ids',False))
        
        if not picking_ids:
            raise Warning(_('No picking found to print'))
        
        if any(picking_ids.filtered(lambda p: p.state != 'done')):
            raise Warning(_('You are trying to print pickings which are not done!'))
        
        if len(picking_ids.mapped('picking_type_id.warehouse_id')) > 1:
            raise Warning(_('Your are trying to print pickings from multiple warehouses!'))
        
        return picking_ids[0].picking_type_id.warehouse_id

    @api.model
    def default_picking_id(self):
        picking_ids = self.env['stock.picking'].browse(self._context.get('active_ids', False))
        for picking in picking_ids:
            return picking

    warehouse_id = fields.Many2one('stock.warehouse', default=default_warehouse)
    picking_id = fields.Many2one('stock.picking', default=default_picking_id)
    waybill_sequence = fields.Char('Sequence', related='warehouse_id.waybill_sequence', readonly=False)
    waybill_number = fields.Integer('Number', related='warehouse_id.waybill_number', readonly=False)

    def print_waybill(self):
        self.ensure_one()

        picking_ids = self.env['stock.picking'].browse(self._context.get('active_ids', False))
        waybill_sequence = self.waybill_sequence
        waybill_number = self.waybill_number

        for picking_id in picking_ids:
            document_number = ','.join(['%s%s' % (waybill_sequence, i) for i in
                                        range(waybill_number, waybill_number + picking_id.document_page_count)])

            picking_id.document_number = document_number
            waybill_number = waybill_number + picking_id.document_page_count

        self.waybill_number = waybill_number

        return self.env.ref('stock_waybill_print.waybill_report')\
            .with_context(active_model='stock_waybill_print.print_waybill_wizard').report_action(docids=self)

