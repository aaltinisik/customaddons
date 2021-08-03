# -*- coding: utf-8 -*-
import logging
from openerp import models, fields, api, _
_logger = logging.getLogger(__name__)

class mass_delete(models.TransientModel):
    _name = 'mass.delete.wiz'
    _description = 'Delete Product'

    @api.multi
    def massdelete_product(self):
        context = dict(self.env.context)
        if context.get('active_ids') and context.get('active_model') == 'product.product':
            active_ids = self.env['product.product'].browse(context.get('active_ids'))
            for product in active_ids:
                productid = product.id
                if product.active:
                    _logger.warning('%s product.product id skipped due to active field is %s' % (str(product.id), product.active))
                    continue
                else:
                    try:
                        product.ean13_ids.unlink()
                        _logger.warning('%s product.product ean13 deleted' % (str(productid)))
                        pass
                    except:
                        _logger.warning('%s product.product EAN13 exception occured could not deleted' % (str(productid)))
                        pass
                    try:
                        product.unlink()
                        self.env.cr.commit()
                        _logger.warning('%s product.product deleted' % (str(productid)))
                        pass
                    except:
                        _logger.warning('%s product.product an exception occured could not deleted' % (str(productid)))
                        self.env.cr.rollback()
                        pass






# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
