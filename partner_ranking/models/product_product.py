from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class Product(models.Model):
    _inherit = 'product.product'

    sale_qty30days = fields.Float('Sale in last 30 days',readonly=True)
    sale_qty180days = fields.Float('Sale in last 180 days',readonly=True)
    sale_qty360days = fields.Float('Sale in last 360 days',readonly=True)

    _defaults = {
        'sale_qty30days': 0.0,
        'sale_qty180days': 0.0,
        'sale_qty360days': 0.0,

    }

    @api.model
    def evaluate_sales(self):
        """
        scheduler for sale count calculations.
        """
        _logger.info("\nScheduler started:: For product sales calculations......................")
        prev_date =str((datetime.now() - timedelta(days=30)).date())
        self._cr.execute('''WITH subquery AS 
                            (SELECT product_id,SUM(product_qty) as total_qty  FROM
                            account_invoice_report WHERE 
                            state not in ('draft', 'cancel','proforma','proforma2') AND
                            type in('out_refund', 'out_invoice') AND
                            date >= '%s'
                            GROUP BY product_id)
                            UPDATE product_product SET sale_qty30days = subquery.total_qty
                            FROM subquery WHERE product_product.id=subquery.product_id
                        ''' %(prev_date))

        prev_date =str((datetime.now() - timedelta(days=180)).date())
        self._cr.execute('''WITH subquery AS 
                            (SELECT product_id,SUM(product_qty) as total_qty  FROM
                            account_invoice_report WHERE 
                            state not in ('draft', 'cancel','proforma','proforma2') AND
                            type in('out_refund', 'out_invoice') AND
                            date >= '%s'
                            GROUP BY product_id)
                            UPDATE product_product SET sale_qty180days = subquery.total_qty
                            FROM subquery WHERE product_product.id=subquery.product_id
                        ''' %(prev_date))
        prev_date =str((datetime.now() - timedelta(days=360)).date())
        self._cr.execute('''WITH subquery AS 
                            (SELECT product_id,SUM(product_qty) as total_qty  FROM
                            account_invoice_report WHERE 
                            state not in ('draft', 'cancel','proforma','proforma2') AND
                            type in('out_refund', 'out_invoice') AND
                            date >= '%s'
                            GROUP BY product_id)
                            UPDATE product_product SET sale_qty360days = subquery.total_qty
                            FROM subquery WHERE product_product.id=subquery.product_id
                        ''' %(prev_date))
        _logger.info("\nScheduler ended:: For product sales calculations......................")
