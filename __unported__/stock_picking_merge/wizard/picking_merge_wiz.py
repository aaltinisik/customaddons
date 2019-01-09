# coding: utf-8

from openerp import api, fields, models, _
from openerp.osv import fields as osv_fields
from openerp.tools import mute_logger
from openerp.osv.orm import browse_record

import psycopg2


class StockPickingMerge(models.TransientModel):
    _name = 'stock.picking.merge'
    _description = 'Merge Pickings'

    destination_picking_id = fields.Many2one('stock.picking', string="Destination Picking")
    source_picking_ids = fields.Many2many('stock.picking', 'picking_merge_rel', 'merge_id', 'picking_id', string="Source Picklings")

    @api.multi
    def _update_refs(self, picking_id, new_picking_id):
        """
        Update all references of moved stock picking  to merged one
        """
        self._update_foreign_keys(picking_id, new_picking_id)
        self._update_reference_fields(picking_id, new_picking_id)
        self._update_values(picking_id, new_picking_id)
        return

    @api.multi
    def get_fk_on(self, table):
        q = """  SELECT cl1.relname as table,
                        att1.attname as column
                   FROM pg_constraint as con, pg_class as cl1, pg_class as cl2,
                        pg_attribute as att1, pg_attribute as att2
                  WHERE con.conrelid = cl1.oid
                    AND con.confrelid = cl2.oid
                    AND array_lower(con.conkey, 1) = 1
                    AND con.conkey[1] = att1.attnum
                    AND att1.attrelid = cl1.oid
                    AND cl2.relname = %s
                    AND att2.attname = 'id'
                    AND array_lower(con.confkey, 1) = 1
                    AND con.confkey[1] = att2.attnum
                    AND att2.attrelid = cl2.oid
                    AND con.contype = 'f'
        """
        self.env.cr.execute(q, (table,))
        return self.env.cr.fetchall()

    @api.multi
    def _update_foreign_keys(self, picking_id, new_picking_id):

        for table, column in self.get_fk_on('stock_picking'):
            if 'stock_picking_merge_' in table:
                continue

            query = "SELECT column_name FROM information_schema.columns WHERE table_name LIKE '%s'" % (table)
            self.env.cr.execute(query, ())
            columns = []
            for data in self.env.cr.fetchall():
                if data[0] != column:
                    columns.append(data[0])

            query_dic = {
                'table': table,
                'column': column,
                'value': columns[0],
            }
            if len(columns) <= 1:
                # unique key treated
                query = """
                    UPDATE "%(table)s" as ___tu
                    SET %(column)s = %%s
                    WHERE
                        %(column)s = %%s AND
                        NOT EXISTS (
                            SELECT 1
                            FROM "%(table)s" as ___tw
                            WHERE
                                %(column)s = %%s AND
                                ___tu.%(value)s = ___tw.%(value)s
                        )""" % query_dic
                self.env.cr.execute(query, (new_picking_id.id, picking_id.id, new_picking_id.id))
            else:
                with mute_logger('openerp.sql_db'), self.env.cr.savepoint():
                    query = 'UPDATE "%(table)s" SET %(column)s = %%s WHERE %(column)s = %%s' % query_dic
                    self.env.cr.execute(query, (new_picking_id.id, picking_id.id,))

    @api.multi
    def _update_reference_fields(self, picking_id, new_picking_id):

        def update_records(model, src, field_model='model', field_id='res_id'):
            try:
                proxy = self.env[model].sudo()
            except KeyError:
                return

            domain = [(field_model, '=', 'stock.picking'), (field_id, '=', src.id)]
            ids = proxy.search(domain)
            try:
                with mute_logger('openerp.sql_db'), self.env.cr.savepoint():

                    return ids.write({field_id: new_picking_id.id})
            except psycopg2.Error:
                # updating fails, most likely due to a violated unique constraint
                # keeping record with nonexistent partner_id is useless, better delete it
                return ids.unlink()

        update_records('ir.attachment', src=picking_id, field_model='res_model')
        update_records('mail.followers', src=picking_id, field_model='res_model')
        update_records('mail.message', src=picking_id)
        update_records('ir.model.data', src=picking_id)
        update_records('calendar', src=picking_id, field_model='model_id.model')

        proxy = self.env['ir.model.fields'].sudo()
        domain = [('ttype', '=', 'reference')]
        record_ids = proxy.search(domain)

        for record in record_ids:
            try:
                proxy_model = self.env[record.model].sudo()
                column = proxy_model._columns[record.name]
            except KeyError:
                # unknown model or field => skip
                continue

            if isinstance(column, osv_fields.function):
                continue

            domain = [
                (record.name, '=', 'stock.picking,%d' % picking_id.id)
            ]
            model_ids = proxy_model.search(domain)
            values = {
                record.name: 'stock.picking,%d' % new_picking_id.id,
            }
            model_ids.write(values)

    @api.multi
    def _update_values(self, picking_id, new_picking_id):
        columns = new_picking_id._columns

        def write_serializer(item):
            if isinstance(item, browse_record):
                return item.id
            else:
                return item

        values = dict()
        for column, field in columns.iteritems():
            if field._type not in ('many2many', 'one2many') and not isinstance(field, osv_fields.function):
                if new_picking_id[column] == False and picking_id[column]:
                    values[column] = write_serializer(picking_id[column])

        values.pop('id', None)

        new_picking_id.write(values)

    @api.onchange('destination_picking_id','source_picking_ids')
    def onchange_destination_picking_id(self):
        domain = [('id','in',self.source_picking_ids.ids)]
        res = {'domain': {'destination_picking_id': domain}}
        if self.env.context.get('active_domain'):
            for picking_type in self.env.context.get('active_domain'):
                if picking_type[0] == 'picking_type_id':
                    domain.extend([('picking_type_id', '=', picking_type[2]), ('state','not in',['done','cancel'])])
                    res['domain'].update({'destination_picking_id': domain})
        return res

    @api.model
    def default_get(self, fields):
        ''' 
        To get default values for the object.
        '''
        res = super(StockPickingMerge, self).default_get(fields)
        res.update({'source_picking_ids': [(6, 0, self.env.context.get('active_ids'))] or []})
        if self.env.context.get('active_ids')[0]:
            res.update({'destination_picking_id': self.env.context.get('active_ids')[0]})
        return res

    @api.multi
    def merge_picking(self):
        picking_ids = []
        skip_ids = []
        for picking in self.source_picking_ids:
            if picking.partner_id.id == self.destination_picking_id.partner_id.id and \
                            picking.picking_type_id.id == self.destination_picking_id.picking_type_id.id and \
                            picking.location_id.id == self.destination_picking_id.location_id.id and \
                            picking.location_dest_id.id == self.destination_picking_id.location_dest_id.id and \
                            picking.invoice_state == self.destination_picking_id.invoice_state and \
                            self.destination_picking_id.id != picking.id:
                picking_ids.append(picking)
            elif self.destination_picking_id.id != picking.id:
                skip_ids.append(picking.id)

        for picking in picking_ids:
            if picking.note:
                if self.destination_picking_id.note:
                    self.destination_picking_id.note += "\n\n" + picking.note
                else:
                    self.destination_picking_id.note = picking.note
            if picking.origin:
                if self.destination_picking_id.origin:
                    self.destination_picking_id.origin += "," + picking.origin
                else:
                    self.destination_picking_id.origin = picking.origin

            self._update_refs(picking, self.destination_picking_id)
            picking.unlink()


        tree_view = self.env.ref('stock.vpicktree')
        form_view = self.env.ref('stock.view_picking_form')
        return {
            'name': 'Picking Merge Results',
            'domain': [('id', 'in', self.destination_picking_id.ids + skip_ids)],
            'res_id': self.destination_picking_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'views': [(tree_view.id, 'tree'), (form_view.id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'current',
            'nodestroy': True
        }