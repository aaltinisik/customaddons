# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models
from odoo.http import request


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # def read(self, fields=None, load="_classic_read"):
    #     res = super(ProductTemplate, self).read(fields=fields, load=load)
    #     excluded_product_ids = request.website.search([]).excluded_product_ids.ids
    #     for product in res:
    #         if product.get("id") in excluded_product_ids and product.get("is_published"):
    #             product["is_published"] = False
    #     return res

    @api.model
    @api.returns(
        "self",
        upgrade=lambda self, value, domain, offset=0, limit=None, order=None, count=False: value
        if count
        else self.browse(value),
        downgrade=lambda self, value, domain, offset=0, limit=None, order=None, count=False: value
        if count
        else value.ids,
    )
    def search(
        self,
        domain,
        offset=0,
        limit=None,
        order=None,
        count=False,
    ):
        if (
            request.is_frontend
            and request.website
            and ("is_published", "=", True) in domain
        ):
            new_domain = []
            for el in domain:
                if el != ("is_published", "=", True):
                    new_domain.append(el)
                else:
                    new_domain.append("&")
                    new_domain.append(el)
                    new_domain.append(
                        (
                            "id",
                            "not in",
                            list(
                                set(
                                    request.website.excluded_product_ids.ids,
                                )
                                | set(
                                    request.website.excluded_product_category_ids.product_tmpl_ids.ids,
                                )
                            ),
                        )
                    )
            domain = new_domain
        return super(ProductTemplate, self).search(
            domain=domain,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
        )
