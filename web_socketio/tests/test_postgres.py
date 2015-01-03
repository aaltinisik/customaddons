# -*- coding: utf-8 -*-

from openerp.tests.common import TransactionCase
from openerp.addons.web_socketio import postgresql
from datetime import datetime, timedelta


class TestPostgres(TransactionCase):

    def test_conn_and_cr_and_gevent_wait_callback(self):
        start = datetime.now()
        db = self.cr.dbname
        conn, cr = postgresql.get_conn_and_cr(db)
        cr.execute("SELECT pg_sleep(5); SELECT 42;")
        postgresql.gevent_wait_callback(cr.connection)
        self.assertEqual(cr.fetchone()[0], 42)
        td = timedelta(seconds=5)
        end = datetime.now()
        if (end - start) < td:
            self.fail("Problème of gevent_wait_callback")
        conn.close()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
