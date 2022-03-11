from odoo import models, api


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.multi
    def render_qweb_pdf(self, res_ids=None, data=None):
        if self.model == 'stock.picking' and res_ids and\
                self.report_name.startswith('altinkaya_reports.report_picking_altinkaya'):
            record_ids = self.env['stock.picking'].browse(res_ids)
            for record in record_ids:
                if record.state not in ['done', 'cancel']:
                    record.action_assign()

        return super(IrActionsReport, self).render_qweb_pdf(res_ids=res_ids, data=data)
