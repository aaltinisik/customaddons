# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    is_published = fields.Boolean(
        string="Is Published",
        help="If checked, the attribute value will be published on the"
             " website.",
        default=False,
    )
    is_default = fields.Boolean(
        string="Is Default",
        help="If checked, the attribute value will be selected by default",
        default=False,
    )

# class ProductAttribute(models.Model):
#     _inherit = "product.attribute"
#
#     def action_create_missing_product_variants(self):
#         """Create missing product variants for published attribute values."""
#         AttributeLineModel = self.env['product.template.attribute.line']
#         filled_variant_ids = []
#         attr_lines = AttributeLineModel.search(
#             [
#                 ('attribute_id', '=', self.id)
#             ]
#         ).filtered(lambda l: len(l.value_ids) < 2)  # get lines with single value
#
#         attr_lines_for_variants = AttributeLineModel
#         for attr_line in attr_lines:
#             tmpl = attr_line.product_tmpl_id.filtered(lambda t: len(t.product_variant_ids) > 1)
#             if len(tmpl.attribute_line_ids) > 1:
#                 attr_lines_for_variants += attr_line
#
#         for attr_line in attr_lines_for_variants:
#             exist_attr = attr_line.value_ids
#             missing_attr = self.value_ids.filtered(lambda v: v != exist_attr)
#
#             variants_to_fill = self.env['product.product'].search(
#                 [
#                     ('product_tmpl_id', '=', attr_line.product_tmpl_id.id),
#                     ('attribute_value_ids', 'not in', exist_attr.ids),
#                 ]
#             )
#             for variant in variants_to_fill:
#                 variant.attribute_value_ids |= missing_attr
#                 filled_variant_ids.append(variant.id)
#
#             attr_line.value_ids |= missing_attr  # write to template also
#
#         return {
#             'name': _('Product Variants'),
#             'view_type': 'tree',
#             'view_mode': 'tree,form',
#             'res_model': 'product.product',
#             'type': 'ir.actions.act_window',
#             'domain': [('id', 'in', filled_variant_ids)],
#         }