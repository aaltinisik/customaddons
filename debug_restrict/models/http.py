# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.tools import ustr
from odoo import exceptions, http, _
import traceback


# Hide traceback from user with monkey patching


def serialize_exception(e):
    if http.request.env.user.has_group("debug_restrict.restrict_debug_mode"):
        debug_log = traceback.format_exc()
    else:
        debug_log = _("Error message is restricted by your system administrator.")
    tmp = {
        "name": type(e).__module__ + "." + type(e).__name__
        if type(e).__module__
        else type(e).__name__,
        "debug": debug_log,
        "message": ustr(e),
        "arguments": e.args,
        "exception_type": "internal_error",
    }
    if isinstance(e, exceptions.UserError):
        tmp["exception_type"] = "user_error"
    elif isinstance(e, exceptions.Warning):
        tmp["exception_type"] = "warning"
    elif isinstance(e, exceptions.RedirectWarning):
        tmp["exception_type"] = "warning"
    elif isinstance(e, exceptions.AccessError):
        tmp["exception_type"] = "access_error"
    elif isinstance(e, exceptions.MissingError):
        tmp["exception_type"] = "missing_error"
    elif isinstance(e, exceptions.AccessDenied):
        tmp["exception_type"] = "access_denied"
    elif isinstance(e, exceptions.ValidationError):
        tmp["exception_type"] = "validation_error"
    elif isinstance(e, exceptions.except_orm):
        tmp["exception_type"] = "except_orm"
    return tmp


# Monkey patching
http.serialize_exception = serialize_exception
