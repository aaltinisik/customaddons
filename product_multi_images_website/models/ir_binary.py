# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api, tools


class IrBinary(models.AbstractModel):
    _inherit = "ir.binary"

    def _get_stream_from(
        self,
        record,
        field_name="raw",
        filename=None,
        filename_field="name",
        mimetype=None,
        default_mimetype="application/octet-stream",
    ):
        """
        Inherited to map new image fields on product.product model since
        we use base_multi_image.image model.
        """
        if record._name == "product.template":
            if field_name == "image_1920":
                field_name = "image_main"
            elif field_name == "image_1024":
                field_name = "image_main"
            elif field_name == "image_512":
                field_name = "image_main"
            elif field_name == "image_256":
                field_name = "image_main_medium"
            elif field_name == "image_128":
                field_name = "image_main_medium"

        return super(IrBinary, self)._get_stream_from(
            record=record,
            field_name=field_name,
            filename=filename,
            filename_field=filename_field,
            mimetype=mimetype,
            default_mimetype=default_mimetype,
        )
