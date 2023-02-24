# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.http_routing.models import ir_http
from unicode_tr.extras import slugify as slugify_tr


def slugify_one(s, max_length=0):
    """
    This method is used to generate a slug from a record or a string while respecting
    the Turkish characters.
    """
    slug_str = slugify_tr(s)
    return slug_str[:max_length] if max_length > 0 else slug_str


def slug(value):
    """
    Since we need to remove id (identifier) from the slug, we need to override this
    """
    try:
        if not value.id:
            raise ValueError("Cannot slug non-existent record %s" % value)
        # [(id, name)] = value.name_get()
        identifier, name = value.id, getattr(value, "seo_name", False) or value.name
    except AttributeError:
        # assume name_search result tuple
        identifier, name = value
    slugname = ir_http.slugify(name or "").strip().strip("-")
    if not slugname:
        return str(identifier)
    return f"{slugname}"


# We need to do monkey patching here.
ir_http.slugify_one = slugify_one
ir_http.slug = slug
