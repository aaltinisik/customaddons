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

    def do_print_package_label(self, cr, uid, ids, op_id=None, context=None):
        '''This function prints the package labels of a single picking'''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        
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
    
    
     
    def printable_packages(self, pack_id=None):
        
        
        package_ids = { v:i+1 for i,v in enumerate(sorted(self.pack_operation_ids.mapped('result_package_id.id')))}
        
        
        operaions = self.pool.get('stock.pack.operation')
        if pack_id:
            operations = self.pack_operation_ids.filtered(lambda po: po.result_package_id.id == pack_id)
        else:
            operations = self.pack_operation_ids.filtered(lambda po: po.result_package_id.id)
        
        res = {}
        
        for op in operations:
            package_data = res.get(op.result_package_id.id, {'no':'%s/%s' % (package_ids[op.result_package_id.id],len(package_ids)),
                                                             'name':op.result_package_id.name,
                                                             'dimensions':'5x5x5 cm',
                                                             'net_weight':'net kg',
                                                             'gross_weight':'gross kg',
                                                             'contents':[]
                                                             })
            package_data['contents'].append({'product':op.product_id.display_name,
                                          'qty':op.qty_done,
                                          'uom':op.product_uom_id.name})
            res.update({op.result_package_id.id:package_data})
            
        return res
    
    def action_print_package(self, cr, uid, ids, pack_id=None, context=None):
        context = dict(context or {}, active_ids=ids, active_model='stock.picking',pack_id=pack_id)
            
#         picking = self.pool.get('stock.picking').browse(cr, uid, ids, context=context)
#         res = picking.printable_packages(pack_id)
#         for k, v in res.items():
#             print v
             
        return self.pool.get("report").get_action(cr, uid, ids, 'warehouse_barcode_interface.aeroo_package_label_print', context=context)
    

     
    
    
    