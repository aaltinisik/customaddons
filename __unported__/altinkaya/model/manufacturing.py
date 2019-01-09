from openerp import models, fields, api, _

class mrp_cancel_more(models.TransientModel):
    _name = 'mrp.cancel.more'


    def cancel_mrp_order(self, cr, uid, ids, context=None):
        """ Cancels the production order and related stock moves.
        @return: True
        """
        if context is None:
            context = {}
        move_obj = self.pool.get('stock.move')
        proc_obj = self.pool.get('procurement.order')

        for production in self.pool.get('mrp.production').browse(cr, uid, context.get('active_ids'), context=context):

            if production.move_created_ids:
                move_obj.action_cancel(cr, uid, [x.id for x in production.move_created_ids])
            procs = proc_obj.search(cr, uid, [('move_dest_id', 'in', [x.id for x in production.move_lines])],
                                    context=context)
            if procs:
                proc_obj.cancel(cr, uid, procs, context=context)
            move_obj.action_cancel(cr, uid, [x.id for x in production.move_lines])
            self.pool.get('mrp.production').write(cr, uid, production.id, {'state': 'cancel'})
        # Put related procurements in exception
        proc_obj = self.pool.get("procurement.order")
        procs = proc_obj.search(cr, uid, [('production_id', 'in', context.get('active_ids'))], context=context)
        if procs:
#            proc_obj.message_post(cr, uid, procs, body=_('Manufacturing order cancelled.'), context=context)
            proc_obj.write(cr, uid, procs, {'state': 'exception'}, context=context)
        return True