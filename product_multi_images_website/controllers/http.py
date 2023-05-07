# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields
from odoo.http import Stream, request
import base64


@classmethod
def from_binary_field_inherit(cls, record, field_name):
    """
    Inherited to map product image fields since
    we're using base_multi_image.image model.

    Note: This is a workaround for Odoo 16.0, it could break some features.
    """
    data_b64 = ""
    if record._name == "product.product":
        variant_images = record.product_tmpl_id.image_ids.filtered(lambda p: record in p.product_variant_ids)
        if variant_images:
            image = variant_images[0]
            data_b64 = image[field_name]
    else:
        data_b64 = record[field_name]

    data = base64.b64decode(data_b64) if data_b64 else b""
    return cls(
        type="data",
        data=data,
        etag=request.env["ir.attachment"]._compute_checksum(data),
        last_modified=record["__last_update"] if record._log_access else None,
        size=len(data),
    )


Stream.from_binary_field = from_binary_field_inherit
