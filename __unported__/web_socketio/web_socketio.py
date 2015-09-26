# -*- coding: utf-8 -*-

from openerp.addons.web.http import session_path
from werkzeug.contrib.sessions import FilesystemSessionStore
from openerp.addons.web_socketio.session import OpenERPRegistry
from openerp.tools import config
from openerp.netsvc import init_logger
from werkzeug.wrappers import Request
from werkzeug.exceptions import NotFound
from logging import getLogger


logger = getLogger(__name__)


class SocketIO(object):

    namespaces = {}

    def __init__(self, args):
        path = session_path()
        self.session_store = FilesystemSessionStore(path)
        self.args = args
        init_logger()
        if args.config_file:
            logger.info("Load OpenERP config file")
            config.parse_config(['-c', args.conf_file])
        self.patch_all()
        databases = args.db
        if not databases:
            database = config.get('db_name', None)
            if not database:
                raise Exception("No database defined")
            databases = [database]
        else:
            databases = databases.split(',')
        self.load_databases(databases, maxcursor=int(args.maxcursor))
        for namespace in self.namespaces.keys():
            logger.info("Add namespace: %r", namespace)

    def patch_all(self):
        from gevent import monkey
        monkey.patch_all()
        from .postgresql import patch
        patch()

    def load_database(self, database, maxcursor=2):
        r = OpenERPRegistry.add(database, maxcursor)
        r.listen()
        r.renotify()

    def load_databases(self, databases, maxcursor=2):
        for db in databases:
            self.load_database(db, maxcursor=maxcursor)

    @classmethod
    def add_namespace(self, namespace, NameSpaceClass):
        assert self.namespaces.get(namespace) is None
        logger.info("Add namespace %r" % namespace)
        self.namespaces[namespace] = NameSpaceClass

    def application(self, environ, start_response):
        path = environ['PATH_INFO']
        if path.startswith('/socket.io/'):
            request = Request(environ)
            from socketio import socketio_manage
            socketio_manage(environ, self.namespaces, request)
        else:
            response = NotFound("Not allowed here only socket.io")
            return response(environ, start_response)

    def serve_forever(self):
        """Load dbs and run gevent wsgi server"""
        from socketio.server import SocketIOServer
        server = SocketIOServer((self.args.interface, int(self.args.port)),
                                self.application, resource="socket.io",
                                policy_server=False)
        logger.info("Start socket.io server %r:%r",
                    self.args.interface, self.args.port)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            for socket in server.sockets.values():
                for namespace in socket.active_ns.values():
                    if hasattr(namespace, 'stop_server'):
                        namespace.stop_server()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
