# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from collections import OrderedDict
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_images(self):
        """Return a list of records implementing `image.mixin` to
        display on the carousel on the website for this variant.

        This returns a list and not a recordset because the records might be
        from different models (template, variant and image).

        It contains in this order: the main image of the variant (if set), the
        Variant Extra Images, and the Template Extra Images.
        """
        self.ensure_one()
        images = self.env["base_multi_image.image"]
        images |= self.product_tmpl_id.image_ids.filtered(
            lambda i: self in i.product_variant_ids
        )
        images |= self.product_tmpl_id._get_images()
        return images
