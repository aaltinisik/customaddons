# -*- encoding: utf-8 -*-


from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import Warning, UserError


class PrintWaybillWizard(models.TransientModel):
    _name = 'stock_waybill_print.print_waybill_wizard'

    warehouse_id = fields.Many2one('stock.warehouse', readonly=True)
    picking_id = fields.Many2one('stock.picking', readonly=True)
    waybill_sequence = fields.Char('Sequence', readonly=False)
    waybill_number = fields.Char('Number', readonly=False)

    @api.model
    def default_get(self, fields_list):
        defaults = super(PrintWaybillWizard, self).default_get(fields_list)
        active_id = self.env.context.get("active_id", False)
        if not active_id:
            raise UserError(_("Please select a picking."))

        picking = self.env["stock.picking"].browse(active_id)

        if picking.state != 'done':
            raise UserError(_("You can only print waybills for done pickings."))

        warehouse_id = picking.picking_type_id.warehouse_id
        if not warehouse_id.waybill_sequence_id:
            raise UserError(_("You need to set a waybill sequence in order to print."))
        defaults['picking_id'] = picking.id
        defaults['warehouse_id'] = warehouse_id.id
        defaults['waybill_sequence'] = 'e'
        defaults['waybill_number'] = warehouse_id.waybill_sequence_id.next_by_id()

        return defaults

    def print_waybill(self):
        self.ensure_one()

        picking_ids = self.env['stock.picking'].browse(self._context.get('active_ids', False))
        waybill_sequence = self.waybill_sequence
        waybill_number = int(self.waybill_number)

        for picking_id in picking_ids:
            document_number = ','.join(['%s%s' % (waybill_sequence, i) for i in
                                        range(waybill_number, waybill_number + picking_id.document_page_count)])

            picking_id.document_number = document_number
            waybill_number = waybill_number + picking_id.document_page_count

        printer = self.warehouse_id.waybill_printer
        if not printer:
            raise Warning(_('You need to set a waybill printer in order to print.'))

        self.warehouse_id.waybill_sequence_id.sudo().write({'number_next_actual': waybill_number})

        printer.print_document('stock_waybill_print.waybill_report',
                               self.env.ref('stock_waybill_print.waybill_report').render_qweb_text([self.id],
                               data={})[0], doc_form="txt")
        return {'type': 'ir.actions.act_window_close'}
