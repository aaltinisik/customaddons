# -*- coding: utf-8 -*-

import gevent_psycopg2
from psycopg2 import extensions, OperationalError, connect
from openerp.sql_db import dsn
from gevent.select import select


def gevent_wait_callback(conn, timeout=None):
    """A wait callback useful to allow gevent to work with Psycopg."""
    while 1:
        state = conn.poll()
        if state == extensions.POLL_OK:
            break
        elif state == extensions.POLL_READ:
            select([conn.fileno()], [], [], timeout=timeout)
        elif state == extensions.POLL_WRITE:
            select([], [conn.fileno()], [], timeout=timeout)
        else:
            raise OperationalError("Bad result from poll: %r" % state)


def patch():
    gevent_psycopg2.monkey_patch()
    extensions.set_wait_callback(gevent_wait_callback)


def get_conn_and_cr(database):
    conn = connect(dsn=dsn(database), async=1)
    gevent_wait_callback(conn)
    cr = conn.cursor()
    return conn, cr

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
