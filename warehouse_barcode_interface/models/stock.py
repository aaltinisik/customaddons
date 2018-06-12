from openerp.osv import fields, osv
from datetime import date, datetime
import time
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT


class stock_picking_type(osv.osv):
    _inherit = "stock.picking.type"

    def _get_picking_counts(self, cr, uid, ids, field_names, arg, context=None):
        obj = self.pool.get('stock.picking')
        domains = {
            'count_picking_draft': [('state', '=', 'draft')],
            'count_picking_waiting': ['|', ('state', '=', 'confirmed'), ('state', 'in', ('assigned', 'partially_available'))],
            'count_picking_ready': [('state', 'in', ('assigned', 'partially_available'))],
            'count_picking': [('state', 'in', ('assigned', 'waiting', 'confirmed', 'partially_available'))],
            'count_picking_late': [('min_date', '<', time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)), ('state', 'in', ('assigned', 'waiting', 'confirmed', 'partially_available'))],
            'count_picking_backorders': [('backorder_id', '!=', False), ('state', 'in', ('confirmed', 'assigned', 'waiting', 'partially_available'))],
        }
        result = {}
        for field in domains:
            data = obj.read_group(cr, uid, domains[field] +
                [('state', 'not in', ('done', 'cancel')), ('picking_type_id', 'in', ids)],
                ['picking_type_id'], ['picking_type_id'], context=context)
            count = dict(map(lambda x: (x['picking_type_id'] and x['picking_type_id'][0], x['picking_type_id_count']), data))
            for tid in ids:
                result.setdefault(tid, {})[field] = count.get(tid, 0)
        for tid in ids:
            if result[tid]['count_picking']:
                result[tid]['rate_picking_late'] = result[tid]['count_picking_late'] * 100 / result[tid]['count_picking']
                result[tid]['rate_picking_backorders'] = result[tid]['count_picking_backorders'] * 100 / result[tid]['count_picking']
            else:
                result[tid]['rate_picking_late'] = 0
                result[tid]['rate_picking_backorders'] = 0
        return result

    _columns = {
        'count_picking_waiting': fields.function(_get_picking_counts,
            type='integer', multi='_get_picking_counts')
    }

class stock_picking(osv.osv):
    _inherit = "stock.picking"

    def do_print_picking_label(self, cr, uid, ids, context=None):
        '''This function prints the picking list'''
        context = dict(context or {}, active_ids=ids)
        return self.pool.get("report").get_action(cr, uid, ids, 'warehouse_barcode_interface.report_picking', context=context)


    def check_for_force_assign(self, cr, uid, ids, context=None):
        for pick in self.pool.get('stock.picking').browse(cr, uid, ids, context=context):
            if pick.state in ['confirmed','waiting','partially_available']:
                return True
            else:
                return False
            
    def get_next_picking_for_ui(self, cr, uid, context=None):
        """ returns the next pickings to process. Used in the barcode scanner UI"""
        if context is None:
            context = {}
        domain = [('state', 'in', ('confirmed','assigned', 'partially_available'))]
        if context.get('default_picking_type_id'):
            domain.append(('picking_type_id', '=', context['default_picking_type_id']))
        return self.search(cr, uid, domain, context=context)
    
    def process_barcode_from_ui(self, cr, uid, picking_id, barcode_str, visible_op_ids, context=None):
        '''This function is called each time there barcode scanner reads an input'''
        def is_upca(code):
            if len(code) == 12 and code.isdigit():
                odd_sum = int(code[0]) + int(code[2]) + int(code[4]) + int(code[6]) + int(code[8]) + int(code[10])
                even_sum = int(code[1]) + int(code[3]) + int(code[5]) + int(code[7]) + int(code[9])
            
                tmp = odd_sum * 3 + even_sum
                parity = 10 - (tmp % 10)
                
                if parity == int(code[11]):
                    return True
                
            return False
                
        
        if is_upca(barcode_str):
            barcode_str = '0%s' % barcode_str
            
        return super(stock_picking, self).process_barcode_from_ui(cr, uid, picking_id, barcode_str, visible_op_ids, context=context)
     
    
    
    