# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api, tools


class BaseMultiImageImage(models.AbstractModel):
    _inherit = "base_multi_image.image"

    image_1920 = fields.Image(
        string="1920", related="image_main", max_width=1920, max_height=1920
    )
    image_1024 = fields.Image(
        string="1024", related="image_main", max_width=1024, max_height=1024
    )
    image_512 = fields.Image(
        string="512", related="image_main", max_width=512, max_height=512
    )
    image_256 = fields.Image(
        string="256", related="image_main", max_width=256, max_height=256
    )
    image_128 = fields.Image(
        string="128", related="image_main", max_width=128, max_height=128
    )

    can_image_1024_be_zoomed = fields.Boolean(
        "Can Image 1024 be zoomed",
        compute="_compute_can_image_1024_be_zoomed",
        store=True,
    )

    @api.depends("image_1920", "image_1024")
    def _compute_can_image_1024_be_zoomed(self):
        """
        Odoo's default zooming mechanism is based on image_1024.
        """
        for image in self:
            image.can_image_1024_be_zoomed = (
                image.image_1920
                and tools.is_image_size_above(image.image_1920, image.image_1024)
            )
