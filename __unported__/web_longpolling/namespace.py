# -*- coding: utf-8 -*-

from openerp.addons.web_socketio.namespace import OpenERPNameSpace
from openerp.addons.web_socketio.session import OpenERPSession
from openerp.addons.web_socketio.web_socketio import SocketIO
from gevent import joinall, killall
from logging import getLogger

logger = getLogger(__name__)


class LongPollingNameSpace(OpenERPNameSpace):

    def __init__(self, *args, **kwargs):
        super(LongPollingNameSpace, self).__init__(*args, **kwargs)
        self.event_started = False

    # dist of the events add to the namespace
    # {event: [(function, adapterClass), ]}
    events = {
        'on': {},
        'connect': {},
        'disconnect': {},
    }

    # for each event the spwan of the function
    activated_events = {}

    @classmethod
    def on(self, event, adapterClass=None, eventtype='on'):
        assert event
        assert isinstance(event, str), "Event must be a string: " + str(event)
        assert eventtype in ('on', 'connect', 'disconnect')
        if adapterClass:
            assert adapterClass.format
            assert adapterClass.get

        def wrapper(function):
            if self.events[eventtype].get(event) is None:
                self.events[eventtype][event] = [(function, adapterClass)]
            else:
                self.events[eventtype][event].append((function, adapterClass))
            logger.info(
                'Add long polling event: %r / %r', event, function.__name__)
            return function
        return wrapper

    def on_session_id(self, session_id):
        super(LongPollingNameSpace, self).on_session_id(session_id)
        if self.event_started and self.uid is not None:
            return
        for event, vals in self.events['connect'].items():
            for function, adapterClass in vals:
                name = function.__module__.split('.')[2]
                session = OpenERPSession(self, adapterClass=adapterClass)
                module = session.model('ir.module.module')
                if module.search([('state', '=', 'installed'),
                                  ('name', '=', name)]):
                    self.spawn(function, session)
                    logger.info("Start connected events %r: %r",
                                event, function.__name__)
        self.event_started = True

    def recv_disconnect(self):
        self.call_disconnect_event()
        super(LongPollingNameSpace, self).recv_disconnect()

    def stop_server(self):
        self.call_disconnect_event()
        super(LongPollingNameSpace, self).stop_server()

    def call_disconnect_event(self):
        disconnect_jobs = []
        for event, vals in self.events['disconnect'].items():
            for function, adapterClass in vals:
                name = function.__module__.split('.')[2]
                session = OpenERPSession(self, adapterClass=adapterClass)
                module = session.model('ir.module.module')
                if module.search([('state', '=', 'installed'),
                                  ('name', '=', name)]):
                    disconnect_jobs.append(self.spawn(function, session))
                    logger.info("Disconnected events %r: %r",
                                event, function.__name__)
        joinall(disconnect_jobs)
        super(LongPollingNameSpace, self).recv_disconnect()
        killall(self.jobs)

    def on_stop_event(self, event):
        jobs = self.activated_events.get(event)
        for job in jobs:
            if job in self.jobs:
                self.jobs.remove(job)

        killall(jobs)

    def process_event(self, packet):
        event = packet['name']
        args = packet['args']
        if self.events['on'].get(event):
            if self.activated_events.get(event) is None:
                self.activated_events[event] = []

            for function, adapterClass in self.events['on'][event]:
                session = OpenERPSession(self, adapterClass=adapterClass)
                self.activated_events[event].append(
                    self.spawn(function, session, *args))
                logger.info("Start %r: %r event ", event, function.__name__)

        elif not hasattr(self, 'on_' + event.replace(' ', '_')):
            self.error('no_such_method',
                       'The method "on_%s" was not found' % event)

        return super(LongPollingNameSpace, self).process_event(packet)


SocketIO.add_namespace('/longpolling', LongPollingNameSpace)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
