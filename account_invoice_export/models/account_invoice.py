

from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT,DEFAULT_SERVER_DATETIME_FORMAT
from openerp import models, fields, api, _


class account_invoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('currency_id', 'amount_total', 'date_export', 'date_invoice')
    def check_amount_total(self):
        if self.currency_id.name == 'TRY':
            self.amount_total_try = self.amount_total
        else:
            export_date = self.date_export if self.date_export else self.date_invoice
            if export_date:
               # print '::ELSEEE', export_date
                user_rec = self.env['res.users'].browse(self._uid)
                lang_format = self.env['res.lang'].search([('code', '=', user_rec.lang)])
                start_export_date = datetime.strptime(export_date, DEFAULT_SERVER_DATE_FORMAT).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                end_export_date = datetime.strptime(export_date, DEFAULT_SERVER_DATE_FORMAT).strftime(DEFAULT_SERVER_DATE_FORMAT) + ' ' + "23:59:00"
                #print '::::export_date', export_date, start_export_date, end_export_date
                currency_ids = self.env['res.currency'].search([('name', '=', 'TRY')], limit=1)
                if currency_ids and start_export_date and end_export_date:
                    self._cr.execute('''SELECT rate FROM res_currency_rate
                                        WHERE currency_id = %s
                                        AND name BETWEEN %s and %s
                                        ORDER BY id DESC LIMIT 1
                                    ''' %(currency_id, start_export_date, end_export_date))
                    [self.cr.fetchall()]
                 #   print '::::currency_rate_ids', currency_rate_ids, currency_rate_ids.rate
                    if currency_rate_ids:
                        self.amount_total_try = self.amount_total * currency_rate_ids.rate

    date_export = fields.Date(string="Date Export")
    amount_total_try = fields.Float(string="Amount Total TRY", compute='check_amount_total', store=True)
    date_invoice = fields.Date(string='Invoice Date',
        readonly=True, states={'draft': [('readonly', False)]}, index=True,
        default=fields.Date.today(),
        help="Keep empty to use the current date", copy=False)


