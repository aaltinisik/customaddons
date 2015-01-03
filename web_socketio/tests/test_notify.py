# -*- coding: utf-8 -*-

from openerp.tests.common import TransactionCase
from ..session import OpenERPRegistry
from gevent import sleep


class TestNotify(TransactionCase):

    def test_notify(self):
        self.r = OpenERPRegistry.add(self.cr.dbname, 2)
        self.r.listen()
        sleep(5)
        notif = self.registry('postgres.notification')
        notif._postgres_channel = 'test'
        notif.notify(self.cr, self.uid, **{'foo': 'bar'})
        sleep(5)
        assert self.r.received_message['test']

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
