# -*- encoding: utf-8 -*-


from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import Warning, UserError


class PrintWaybillWizard(models.TransientModel):
    _name = 'stock_waybill_print.print_waybill_wizard'

    warehouse_id = fields.Many2one('stock.warehouse', readonly=True)
    picking_id = fields.Many2one('stock.picking', readonly=True)
    waybill_sequence = fields.Char('Sequence', readonly=False)
    waybill_number = fields.Integer('Number', readonly=False)

    @api.model
    def default_get(self, fields_list):
        defaults = super(PrintWaybillWizard, self).default_get(fields_list)
        active_id = self.env.context.get("active_id", False)
        if not active_id:
            raise UserError(_("Please select a picking."))

        picking = self.env["stock.picking"].browse(active_id)
        defaults['picking_id'] = picking.id
        defaults['warehouse_id'] = picking.picking_type_id.warehouse_id.id
        defaults['waybill_sequence'] = 'e'
        defaults['waybill_number'] = int(self.env['ir.sequence'].next_by_code('res.partner'))

        return defaults

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
        printer = self.warehouse_id.waybill_printer
        if not printer:
            raise Warning(_('You need to set a waybill printer in order to print.'))
        printer.print_document('stock_waybill_print.waybill_report',
                               self.env.ref('stock_waybill_print.waybill_report').render_qweb_text([self.id],
                               data={})[0], doc_form="txt")
        return {'type': 'ir.actions.act_window_close'}
