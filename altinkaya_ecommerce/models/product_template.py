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
        help="Files publicly downloadable from the product eCommerce page.",
    )

    # @api.model
    # def _domain_website_attachment_ids(self):
    #     """Get domain for website attachments."""
    #     ctx_params = self.env.context.get('params', {})
    #     domain = []
    #
    #     if ctx_params.get('id', False):
    #         domain += [('res_id', '=', ctx_params['id'])]
    #
    #     if ctx_params.get('model', False):
    #         domain += [('res_model', '=', ctx_params['model'])]
    #
    #     return domain

    @api.multi
    def write(self, vals):
        """Prevent saving attributes with single value."""
        res = super(ProductTemplate, self).write(vals)

        for attr_line in self.mapped(lambda p: p.attribute_line_ids):
            if attr_line.required and len(attr_line.value_ids.ids) < 2:
                raise ValidationError(_("You can not save required attributes"
                                        "with single value. %s "
                                        % attr_line.attribute_id.display_name))
        return res

    def action_fill_missing_product_attrs(self):
        """Fill missing product variants for published attribute values."""
        if len(self.product_variant_ids) == 1:
            raise ValidationError(_("You can not fill missing product of non"
                                    " variant product."))

        tmpl_attribute_lines = self.attribute_line_ids.filtered(lambda x: x.required)
        required_attrs = tmpl_attribute_lines.mapped('attribute_id')
        filled_variant_ids = []

        for product in self.product_variant_ids:
            product_attrs = product.attribute_value_ids.mapped('attribute_id')
            if not all(x in product_attrs.ids for x in required_attrs.ids):
                missing_attrs = required_attrs - product_attrs
                for attr in missing_attrs:
                    tmpl_line = tmpl_attribute_lines.filtered(lambda l: l.attribute_id == attr)

                    default_attr_value = attr.value_ids.filtered(lambda v: v.is_default)
                    if not default_attr_value:
                        raise ValidationError(_(
                            "Set default value for attribute %s"
                            % attr.name
                        ))
                    product.attribute_value_ids |= default_attr_value
                    tmpl_line.value_ids |= default_attr_value
                    filled_variant_ids.append(product.id)

        if not filled_variant_ids:
            raise ValidationError(_("No missing product variants found."))

        tree_view_id = self.env.ref('product.product_product_tree_view').id
        action = {
            'type': 'ir.actions.act_window',
            'views': [(tree_view_id, 'tree')],
            'view_mode': 'tree,form',
            'name': _('Products'),
            'res_model': 'product.product',
            'domain': "[('type', '=', 'product'), ('id', 'in', %s)]"
                      % filled_variant_ids,
        }
        return action