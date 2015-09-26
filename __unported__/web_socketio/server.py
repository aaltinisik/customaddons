# -*- coding: utf-8 -*-

from openerp.addons.web_socketio.web_socketio import SocketIO
from argparse import ArgumentParser


def run():
    parser = ArgumentParser(description='Gevent WSGI server')
    parser.add_argument('-d', dest='db', default='',
                        help="'list of db names, separated by ','")
    parser.add_argument('-i', dest='interface', default='127.0.0.1',
                        help="Define the interface to listen")
    parser.add_argument('-p', dest='port', default=8068,
                        help="Define the port to listen")
    parser.add_argument('-c', dest='config_file', default='',
                        help="Config file of openerp use for addons_path")
    parser.add_argument('--max-cursor', dest='maxcursor', default=2,
                        help="Max declaration of cursor by data base")

    args = parser.parse_args()
    socketio = SocketIO(args)
    socketio.serve_forever()

if __name__ == '__main__':
    run()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
