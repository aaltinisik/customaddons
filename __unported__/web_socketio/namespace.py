# -*- coding: utf-8 -*-

from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
from openerp.addons.web_socketio.session import OpenERPRegistry, OpenERPObject
from werkzeug.contrib.sessions import FilesystemSessionStore
from openerp.addons.web.http import session_path
from logging import getLogger

logger = getLogger(__name__)


class OpenERPNameSpace(BaseNamespace, BroadcastMixin):

    def recv_connect(self):
        logger.info("Connection open with the socket %r (%r)",
                    self.socket, self.ns_name)
        self.emit('get session id')

    def recv_disconnect(self):
        if self.database:
            registry = OpenERPRegistry.get(self.database)
            for channel, sockets in registry.selected_received_message.items():
                if sockets.get(self.socket):
                    while registry.selected_received_message[channel][self.socket]:
                        m = registry.selected_received_message[channel][
                            self.socket].pop(0)
                        registry.received_message[channel].append(m)

        logger.info("Connexion close for the socket %r", self.socket)
        super(OpenERPNameSpace, self).recv_disconnect()

    def stop_server(self):
        logger.info(
            "Connexion close by the server for the socket %r", self.socket)

    def get_initial_acl(self):
        """ Only on_session_id can be called """
        return ['on_session_id', 'recv_connect', 'recv_disconnect']

    def on_session_id(self, session_id):
        """ sockectio_manage can call all the event only if the session is
        validate"""
        path = session_path()
        session_store = FilesystemSessionStore(path)
        sid = self.request.cookies.get('sid')
        session = None
        self.uid = None
        if sid:
            session = session_store.get(sid)

        if session and session_id:
            session = session.get(session_id)
        else:
            session = None

        if not session:
            return

        session.assert_valid()
        self.context = session.context
        self.uid = session._uid
        self.database = session._db
        self.lift_acl_restrictions()

    def model(self, obj):
        return OpenERPObject(OpenERPRegistry.get(self.database), self.uid, obj)

    def listen(self, adapterClass, *args, **kwargs):
        return adapterClass(OpenERPRegistry.get(self.database),
                            self.socket).listen(*args, **kwargs)

    def validate(self, adapterClass, issend):
        adapterClass(OpenERPRegistry.get(self.database),
                     self.socket).validate(issend)

    def secure_emit(self, adapterClass, event, *args, **kwargs):
        try:
            if self.socket.state != self.socket.STATE_CONNECTED:
                raise Exception('Not connected')
            self.emit(event, *args, **kwargs)
            self.validate(adapterClass, True)
        except:
            self.validate(adapterClass, False)

    def notify(self, channel, **kwargs):
        OpenERPRegistry.get(self.database).notify(channel, self.uid, **kwargs)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
