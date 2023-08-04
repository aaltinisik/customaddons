# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, api
from odoo.tools import html_escape as escape
from collections import OrderedDict
from markupsafe import Markup
from odoo.tools import pycompat


class Image(models.AbstractModel):
    _inherit = "ir.qweb.field.image"

    @api.model
    def record_to_html(self, record, field_name, options):
        """
        Override to add lightbox support to product images on website.
        Add lightbox: True to the options dict to enable lightbox.
        """
        assert options["tagName"] != "img", (
            "Oddly enough, the root tag of an image field can not be img. "
            "That is because the image goes into the tag, or it gets the "
            "hose again."
        )

        if options.get("qweb_img_raw_data", False):
            return super(Image, self).record_to_html(record, field_name, options)

        aclasses = (
            ["img", "img-fluid"]
            if options.get("qweb_img_responsive", True)
            else ["img"]
        )
        aclasses += options.get("class", "").split()
        classes = " ".join(map(escape, aclasses))

        src, src_zoom = self._get_src_urls(record, field_name, options)

        if options.get("alt-field") and getattr(record, options["alt-field"], None):
            alt = escape(record[options["alt-field"]])
        elif options.get("alt"):
            alt = options["alt"]
        else:
            alt = escape(record.display_name)

        itemprop = None
        if options.get("itemprop"):
            itemprop = options["itemprop"]

        lightbox_compatible = field_name != "image_128" and options.get(
            "lightbox", False
        )

        atts = OrderedDict()
        atts["src"] = src
        atts["itemprop"] = itemprop
        atts["class"] = classes
        atts["style"] = options.get("style")
        atts["width"] = options.get("width")
        atts["height"] = options.get("height")
        atts["alt"] = alt

        # since we are using lightbox, we don't need the zoom image
        if not lightbox_compatible:
            atts["data-zoom"] = src_zoom and "1" or None
            atts["data-zoom-image"] = src_zoom

        atts["data-no-post-process"] = options.get("data-no-post-process")

        atts = self.env["ir.qweb"]._post_processing_att("img", atts)

        img = ["<img"]
        for name, value in atts.items():
            if value:
                img.append(" ")
                img.append(escape(pycompat.to_text(name)))
                img.append('="')
                img.append(escape(pycompat.to_text(value)))
                img.append('"')
        img.append("/>")

        # Wrap the image in "a" tag .to make it Lightbox compatible
        # Filter out the image_128 field
        if lightbox_compatible:
            img = (
                [
                    '<a href="',
                    src_zoom or src,
                    '" data-lightbox="product_image',
                    '" data-title="',
                    escape(record.name),
                    '">',
                ]
                + img
                + ["</a>"]
            )

        return Markup("".join(img))
