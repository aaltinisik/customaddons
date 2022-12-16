# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.translate import html_translate


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_published = fields.Boolean(
        string="Is Published",
        help="If checked, the product will be published on the website.",
        default=False,
    )

    public_description = fields.Html(
        "Description for e-Commerce",
        sanitize_attributes=False,
        translate=html_translate,
        copy=False)

    website_attachment_ids = fields.Many2many(
        string="Website attachments",
        comodel_name="ir.attachment",
        domain=lambda self, *args, **kwargs: (
            self._domain_website_attachment_ids(*args, **kwargs)
        ),
        help="Files publicly downloadable from the product eCommerce page.",
    )

    @api.model
    def _domain_website_attachment_ids(self):
        """Get domain for website attachments."""
        ctx_params = self.env.context.get('params', {})
        domain = []

        if ctx_params.get('id', False):
            domain += [('res_id', '=', ctx_params['id'])]

        if ctx_params.get('model', False):
            domain += [('res_model', '=', ctx_params['model'])]

        return domain

    @api.multi
    def write(self, vals):
        """Prevent saving attributes with single value."""
        res = super(ProductTemplate, self).write(vals)

        for attr_line in self.mapped(lambda p: p.attribute_line_ids):
            if len(attr_line.value_ids.ids) < 2:
                raise ValidationError(_("You can not save attributes"
                                        " with single value. %s "
                                        % attr_line.attribute_id.display_name))
        return res
