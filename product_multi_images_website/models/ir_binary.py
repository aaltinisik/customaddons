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
        image_mapping = {
            "image_1920": "image_main",
            "image_1024": "image_main",
            "image_512": "image_main",
            "image_256": "image_main_medium",
            "image_128": "image_main_medium",
        }
        # Replace product.image with base_multi_image.image
        # if record._name == "product.image":
        #     tmpl_first_img = fields.first(
        #         record.product_tmpl_id.image_ids.filtered(
        #             lambda i: i.is_published and i.bind_ids
        #         )
        #     )
        #     if tmpl_first_img:
        #         record = tmpl_first_img

        if record._name == "product.template" and not getattr(record, field_name):
            try:
                field_name = image_mapping[field_name]
            except KeyError:
                pass

        return super(IrBinary, self)._get_stream_from(
            record=record,
            field_name=field_name,
            filename=filename,
            filename_field=filename_field,
            mimetype=mimetype,
            default_mimetype=default_mimetype,
        )
