# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import http
import traceback
from odoo.tools import ustr


def serialize_exception(exception):
    """
    If the user is in the debug group, return the full traceback
    If not, return a restricted message
    """
    name = type(exception).__name__
    module = type(exception).__module__

    if http.request.env.user.has_group("website_debug_restrict.restrict_debug_mode"):
        debug_log = traceback.format_exc()
    else:
        debug_log = "Restricted"
    return {
        "name": f"{module}.{name}" if module else name,
        "debug": debug_log,
        "message": ustr(exception),
        "arguments": exception.args,
        "context": getattr(exception, "context", {}),
    }


# Monkey patching
http.serialize_exception = serialize_exception
