# -*- coding: utf-8 -*-

from openerp.tests.common import TransactionCase
from ..session import OpenERPRegistry, AbstractAdapter
from ..notify import get_channel
from simplejson import dumps
from gevent import sleep


class Adapter(AbstractAdapter):
    channel = 'test'


class TestOpenERPRegistry(TransactionCase):

    def tearDown(self):
        super(TestOpenERPRegistry, self).tearDown()
        OpenERPRegistry.registries = {}

    def setUp(self):
        super(TestOpenERPRegistry, self).setUp()
        self.r = OpenERPRegistry.add(self.cr.dbname, 2)

    def test_adapter(self):
        self.r.listen()
        message = dumps({
            'channel': 'test',
            'uid': self.uid,
            'values': {
                'uid': self.uid,
            },
        })
        sleep(.1)
        self.cr.execute('NOTIFY ' + get_channel() + ', %s;', (message,))
        self.cr.commit()
        sleep(0)
        messages = Adapter(self.r, 'socket').listen()
        assert messages
        assert messages[0]['uid'] == self.uid
        assert not self.r.received_message['test']

    def test_notify(self):
        self.r.listen()
        sleep(0.1)
        self.r.notify('test', self.uid, uid2=self.uid)
        sleep(0)
        messages = Adapter(self.r, 'socket').listen()
        assert messages
        assert messages[0]['uid2'] == self.uid
        assert not self.r.received_message['test']

    def test_validate_True(self):
        self.r.received_message['test'] = []
        self.r.selected_received_message['test'] = {'socket': ['test']}
        Adapter(self.r, 'socket').validate(True)
        assert len(self.r.selected_received_message['test']['socket']) == 0
        assert len(self.r.received_message['test']) == 0

    def test_validate_False(self):
        self.r.received_message['test'] = []
        self.r.selected_received_message['test'] = {'socket': ['test']}
        Adapter(self.r, 'socket').validate(False)
        assert len(self.r.selected_received_message['test']['socket']) == 0
        assert len(self.r.received_message['test']) == 1
        assert self.r.received_message['test'][0] == 'test'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
