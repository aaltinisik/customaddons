# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.http_routing.models import ir_http
from unicode_tr.extras import slugify as slugify_tr


def slug_tr(value):
    """
    This method is used to generate a slug from a record or a string while respecting
    the Turkish characters.
    The original method is copied from odoo.addons.http_routing.models.ir_http
    """
    try:
        if not value.id:
            raise ValueError("Cannot slug non-existent record %s" % value)
        # [(id, name)] = value.name_get()
        identifier, name = (
            value.id,
            getattr(value, "seo_name", False) or value.display_name,
        )
    except AttributeError:
        # assume name_search result tuple
        identifier, name = value
    slugname = slugify_tr(name or "").strip().strip("-")
    if not slugname:
        return str(identifier)
    return f"{slugname}-{identifier}"


ir_http.slug = slug_tr
