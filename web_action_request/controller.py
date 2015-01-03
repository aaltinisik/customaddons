# -*- coding: utf-8 -*-

from openerp.addons.web_longpolling.namespace import LongPollingNameSpace
from openerp.addons.web_socketio.session import AbstractAdapter


class RequestAdapter(AbstractAdapter):
    channel = 'action.request'

    def get(self, messages, uid):
        res = []
        for m in messages:
            if m['values']['to_id'] == uid:
                res.append(m)
        return res


@LongPollingNameSpace.on(
    'get request', adapterClass=RequestAdapter, eventtype='connect')
def get_request(session):
    while True:
        request = session.listen(session.uid)
        session.validate(True)
        session.emit('get request', request[0])
