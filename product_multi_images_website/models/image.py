# © 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3).

from odoo import api, fields, models


class Image(models.Model):
    _inherit = "base_multi_image.image"

    is_published = fields.Boolean(
        string="Is published",
        default=True,
        help="If you leave it empty, all variants will show this image. "
        "Selecting one or several of the available variants, you "
        "restrict the availability of the image to those variants.",
    )
