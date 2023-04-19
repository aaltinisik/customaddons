# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    next_product = fields.Many2one(
        "product.template",
        string="Next Product",
        compute="_compute_next_previous_product",
    )

    previous_product = fields.Many2one(
        "product.template",
        string="Previous Product",
        compute="_compute_next_previous_product",
    )

    """
    In website_sale module "featured" sort is reversed. So don't worry about the
    computation with wrong domains.
    """

    def _compute_next_previous_product(self):
        self.ensure_one()
        website_id = self.env["website"].get_current_website()
        query = """
                SELECT 
          pt.id, 
          pt.website_sequence, 
          pt.is_published, 
          pt.categ_id, 
          pt.website_id, 
          pt.sub_component
        FROM 
          product_template AS pt 
          JOIN product_public_category_product_template_rel AS rel ON pt.id = rel.product_template_id 
          JOIN product_public_category AS ppc ON rel.product_public_category_id = ppc.id 
          JOIN product_category AS pc ON pt.categ_id = pc.id 
        WHERE 
          pt.sale_ok = TRUE 
          AND pc.is_published = TRUE 
          AND pt.is_published = TRUE 
          AND pt.sub_component = FALSE 
          AND ppc.id IN %s
          AND (
            pt.website_id = %s 
            OR pt.website_id IS NULL
          )
          ORDER BY pt.is_published desc, pt.website_sequence asc, pt.id desc
          ;
        """

        self.env.cr.execute(query, (tuple(self.public_categ_ids.ids), website_id.id))
        results = self.env.cr.dictfetchall()
        ordered_ids = [result["id"] for result in results]

        # Find the previous and next product ids in the ordered list
        current_index = ordered_ids.index(self.id)
        previous_index = current_index - 1
        next_index = current_index + 1
        self.previous_product = (
            ordered_ids[previous_index] if previous_index >= 0 else False
        )
        self.next_product = (
            ordered_ids[next_index] if next_index < len(ordered_ids) else False
        )
        return True

