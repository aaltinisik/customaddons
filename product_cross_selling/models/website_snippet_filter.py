# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, api, fields
from odoo.osv import expression


class WebsiteSnippetFilter(models.Model):
    _inherit = "website.snippet.filter"

    def _get_products_alternative_products(self, website, limit, domain, context):
        """
        Override to get related products. Related products are products that have
        the same public category as the current product and are not in the cart.
        """
        products = self.env["product.product"]
        current_id = context.get("product_template_id")
        if not current_id:
            return products
        current_template = self.env["product.template"].browse(int(current_id))
        if current_template.exists():
            # Exlude current product and products in the cart
            excluded_products = website.sale_get_order().mapped("order_line.product_id")
            excluded_products |= current_template.product_variant_ids
            related_products = self._get_related_products(current_template, domain)
            products = related_products - excluded_products
            if products:
                domain = expression.AND(
                    [
                        domain,
                        [("id", "in", products.ids)],
                    ]
                )
                products = (
                    self.env["product.product"]
                    .with_context(display_default_code=False)
                    .search(domain, limit=limit, order="website_sequence asc")
                )
        # Filter out "No combination available" products
        # This method looks tricky, but it's the fastest (?) way to do it
        return products.filtered(lambda p: p._get_contextual_price_tax_selection())

    def _get_related_products(self, current_template, domain):
        """
        Get related products. Order by website sequence.
        """
        products = self.env["product.product"]
        public_categ_ids = current_template.public_categ_ids
        domain = expression.AND(
            [
                domain,
                [
                    ("public_categ_ids", "in", public_categ_ids.ids),
                    ("id", "!=", current_template.id),
                ],
            ]
        )
        tmpl_ids = self.env["product.template"].search(
            domain, order="website_sequence asc", limit=20
        )
        for tmpl in tmpl_ids:
            if tmpl.default_variant_id:
                products |= tmpl.default_variant_id
            else:
                variant = next(
                    (
                        variant
                        for variant in tmpl.product_variant_ids
                        if not any(
                            comb == "hidden"
                            for comb in variant.mapped(
                                "product_template_attribute_value_ids.attribute_id.visibility"
                            )
                        )
                    ),
                    None,
                )
                if variant:
                    products |= variant
        return products
