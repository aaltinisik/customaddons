# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class MrpBomTemplateLine(models.Model):
    _name = "mrp.bom.template.line"
    _description = "Mrp Bom Template Lines"
    _order = "sequence, id"

    name = fields.Char(
        string="Name",
        related="product_tmpl_id.name",
        readonly=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=100,
    )
    bom_id = fields.Many2one(
        "mrp.bom",
        string="Bom Template",
    )
    product_tmpl_id = fields.Many2one(
        "product.template",
        string="Product Template",
        required=True,
    )
    product_qty = fields.Float(
        string="Quantity",
        default=1.0,
        required=True,
    )
    product_uom_id = fields.Many2one(
        "uom.uom",
        string="Unit of Measure",
        required=True,
        default=lambda self: self.env.ref("uom.product_uom_unit"),
    )
    inherited_attribute_id = fields.Many2one(
        "product.attribute",
        string="Inherited Attribute",
    )
    applied_on_variants = fields.Many2many(
        "product.product",
        string="Applied on Variants",
    )

    @api.onchange("product_tmpl_id")
    def _product_onchange_domain(self):
        """
        Filter out the inherited attributes of the product template
        :return: context dict with domain
        """
        vals = []
        if self.product_tmpl_id:
            vals = [
                (
                    "id",
                    "in",
                    self.product_tmpl_id.mapped("attribute_line_ids.attribute_id").ids,
                )
            ]
        domain = {"domain": {"inherited_attribute_id": vals}}
        return domain
