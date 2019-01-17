

from odoo import models,fields,api

class mrp_cancel_more(models.TransientModel):
    _name = 'mrp.cancel.more'



    #should check what is this doing onur

    @api.multi
    def cancel_mrp_order(self):
        """ Cancels the production order and related stock moves.
        @return: True
        """
        move_obj = self.env['stock.move']
        active_ids=self._context.get('active_ids',False)
        productions=self.env['mrp.production'].browse(active_ids)
        for production in productions:
            if production.move_created_ids:
                move_obj.action_cancel([x.id for x in production.move_created_ids])
            move_obj.action_cancel( [x.id for x in production.move_lines])
            production.write({'state': 'cancel'})
        return True