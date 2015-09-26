# -*- coding: utf-8 -*-

from openerp.osv import osv
from openerp.tools import config
from openerp.modules.registry import RegistryManager
from simplejson import dumps
from datetime import datetime


def get_channel():
    return config.get('longpolling_channel', 'longpolling_channel')


class PostgresNotification(osv.AbstractModel):
    _name = 'postgres.notification'
    _description = 'AbstractClass to notify'
    _postgres_channel = None

    def notify(self, cr, uid, **kwargs):
        assert self._postgres_channel
        cursor = RegistryManager.get(cr.dbname).db.cursor()
        message = dumps({
            'channel': self._postgres_channel,
            'uid': uid,
            'date': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
            'values': kwargs,
        })
        cursor.execute('NOTIFY ' + get_channel() + ', %s;', (message,))
        cursor.commit()
        cursor.close()

    def committed_notify(self, cr, uid, **kwargs):
        assert self._postgres_channel
        message = dumps({
            'channel': self._postgres_channel,
            'uid': uid,
            'date': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
            'values': kwargs,
        })
        cr.execute('NOTIFY ' + get_channel() + ', %s;', (message,))

    def renotify(self, cr, uid, context=None):
        ''' Hook use by the socketio server

        If the model has this method so the method is call to renotify
        Use to renotify after the restart of the server'''
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
