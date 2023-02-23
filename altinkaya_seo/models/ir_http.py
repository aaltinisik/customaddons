# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.http_routing.models import ir_http
from unicode_tr.extras import slugify as slugify_tr


def slugify_one(s, max_length=0):
    """
    This method is used to generate a slug from a record or a string while respecting
    the Turkish characters.
    The original method is copied from odoo.addons.http_routing.models.ir_http
    """
    slug_str = slugify_tr(s)
    return slug_str[:max_length] if max_length > 0 else slug_str


ir_http.slugify_one = slugify_one
