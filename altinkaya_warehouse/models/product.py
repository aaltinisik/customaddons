
from openerp import models, fields, api, _


class product_template(models.Model):
    _inherit = "product.template"

    pop_bom_in_reports = fields.Boolean(string="Populate BOM in Picking Report")
