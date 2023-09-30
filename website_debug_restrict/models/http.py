# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import http


def _response(self, result=None, error=None):
    """
    If the user is in the debug group, return the full traceback
    If not, return a restricted message
    """
    response = {"jsonrpc": "2.0", "id": self.request_id}
    if error is not None:
        if not self.request.env.user.has_group(
            "website_debug_restrict.restrict_debug_mode"
        ):
            response["result"] = {"error": "Restricted."}
        else:
            response["error"] = error
    if result is not None:
        response["result"] = result
    return self.request.make_json_response(response)


# Monkey patching
http.JsonRPCDispatcher._response = _response
