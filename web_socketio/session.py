# -*- coding: utf-8 -*-

from contextlib import contextmanager
from openerp.addons.web_socketio.notify import get_channel
from openerp.modules.registry import RegistryManager
from .postgresql import gevent_wait_callback, get_conn_and_cr
from gevent import spawn, sleep
from simplejson import loads, dumps
from psycopg2 import Error
from datetime import datetime


class AbstractAdapter(object):
    # FIXME what append during the disconnection of a socket
    # The adapter should move the message from selected_received_message to
    # received_message

    channel = None
    sleeptime = 0.01

    def __init__(self, registry, socket):
        self.registry = registry
        self.socket = socket
        assert self.channel

    def get(self, messages, *args, **kwargs):
        """ Return the messageto get """
        res = []
        for m in messages:
            res.append(m)
        return res

    def format(self, message, *args, **kwargs):
        return message['values']

    def listen(self, *args, **kwargs):

        def compare(x, y):
            if x['date'] < y['date']:
                return -1
            if x['date'] > y['date']:
                return 1
            return 0

        while True:
            sleep(self.sleeptime)  # switch to other coroutine
            received_messages = self.registry.received_message.get(
                self.channel, [])
            if not received_messages:
                continue
            messages = self.get(received_messages, *args, **kwargs)
            if not messages:
                continue
            result = []
            messages.sort(cmp=compare)
            for message in messages:
                if self.registry.selected_received_message.get(self.channel) is None:
                    self.registry.selected_received_message[self.channel] = {}

                if self.registry.selected_received_message[self.channel].get(self.socket) is None:
                    self.registry.selected_received_message[self.channel][self.socket] = []

                self.registry.selected_received_message[self.channel][
                    self.socket].append(message)
                self.registry.received_message[self.channel].remove(message)
                result.append(self.format(message, *args, **kwargs))

            return result

    def validate(self, issend):
        while self.registry.selected_received_message[self.channel][self.socket]:
            m = self.registry.selected_received_message[self.channel][
                self.socket].pop(0)
            if not issend:
                self.registry.received_message[self.channel].append(m)


class OpenERPObject(object):

    def __init__(self, registry, uid, model):
        self.registry = registry
        self.uid = uid
        self.obj = registry.registry.get(model)

    def __getattr__(self, fname):
        def wrappers(*args, **kwargs):
            with self.registry.cursor() as cr:
                return getattr(self.obj, fname)(cr, self.uid, *args, **kwargs)
        return wrappers


class OpenERPRegistry(object):

    registries = {}  # {db: cls}

    def __init__(self, database, maxcursor):
        self.registry = RegistryManager.get(database)
        self.maxcursor = maxcursor
        self.received_message = {}
        self.selected_received_message = {}

    @classmethod
    def add(cls, database, maxcursor):
        r = cls(database, maxcursor)
        cls.registries[database] = r
        return r

    @classmethod
    def get(cls, database):
        if database not in cls.registries.keys():
            return cls.add(database, 2)
        return cls.registries[database]

    def get_openerpobject(self, uid, model):
        return OpenERPObject(self, uid, model)

    def listen(self):
        self.maxcursor -= 1
        conn, cr = get_conn_and_cr(self.registry.db_name)
        cr.execute('Listen ' + get_channel() + ';')

        def get_listen():
            while True:
                gevent_wait_callback(cr.connection)
                while conn.notifies:
                    notify = conn.notifies.pop()
                    payload = loads(notify.payload)
                    channel = payload['channel']
                    del payload['channel']
                    if self.received_message.get(channel) is None:
                        self.received_message[channel] = []
                    self.received_message[channel] += [payload]

                sleep(0.001)  # switch yo other coroutine

        spawn(get_listen)

    @contextmanager
    def cursor(self):
        while self.maxcursor <= 0:
            sleep(0)
        try:
            self.maxcursor -= 1
            cursor = self.registry.db.cursor(serialized=False)
            yield cursor
            cursor.commit()
        except Error:
            self.rollback()
        finally:
            cursor.close()
            self.maxcursor += 1

    def notify(self, channel, uid, **kwargs):
        with self.cursor() as cr:
            message = dumps({
                'channel': channel,
                'uid': uid,
                'date': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
                'values': kwargs,
            })
            cr.execute('NOTIFY ' + get_channel() + ', %s;', (message,))
        return True

    def renotify(self):
        model_obj = self.get_openerpobject(1, 'ir.model')
        m_ids = model_obj.search([])
        for m in model_obj.read(m_ids, ['model']):
            obj = self.get_openerpobject(1, m['model'])
            if hasattr(obj.obj, 'renotify'):
                obj.renotify()


class OpenERPSession(object):

    def __init__(self, namespace, adapterClass=None):
        self.adapterClass = adapterClass
        self.namespace = namespace
        self.uid = namespace.uid
        self.context = namespace.context

    def __getattr__(self, fname):
        def wrappers(*args, **kwargs):
            if fname in ('listen', 'validate', 'secure_emit'):
                if not self.adapter:
                    raise Exception("No Adapter defined for the listen action")
                return getattr(self.namespace, fname)(
                    self.adapterClass, *args, **kwargs)
            else:
                return getattr(self.namespace, fname)(*args, **kwargs)
        return wrappers


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
