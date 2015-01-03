# -*- coding: utf-8 -*-

from . import test_postgres
from . import test_registry
from . import test_notify

fast_suite = [
    test_postgres,
    test_registry,
    test_notify,
]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
