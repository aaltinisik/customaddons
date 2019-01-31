# Copyright (C) 2014-TODAY GRAP (http://www.grap.coop)
# Copyright (C) 2016-TODAY La Louve (http://www.lalouve.net)
# Copyright 2017 LasLabs Inc.
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import UserError



class BarcodeGenerateMixin(models.AbstractModel):
    _inherit = 'barcode.generate.mixin'


#     @api.model
#     def create(self, vals):
#         """It creates a new barcode if automation is active."""
#         barcode_rule = self.env['barcode.rule'].get_automatic_rule(self._name)
#         if barcode_rule.exists():
#             vals.update({
#                 'barcode_rule_id': barcode_rule.id,
#             })
#         record = super(BarcodeGenerateMixin, self).create(vals)
#         if barcode_rule:
#             record.generate_base()
#             record.generate_barcode()
#         return record

    # View Section
    @api.multi
    def generate_base(self):
        if self._name == 'product.product':
            for item in self:
                if item.generate_type != 'sequence':
                    raise UserError(_(
                        "Generate Base can be used only with barcode rule with"
                        " 'Generate Type' set to 'Base managed by Sequence'"))
                elif item.product_tmpl_id.barcode_rule_id:
                    item.barcode_base =item.product_tmpl_id.barcode_rule_id.sequence_id.next_by_id()
                else:
                    item.barcode_base = item.categ_id.barcode_rule_id.sequence_id.next_by_id()
        else:
            super(BarcodeGenerateMixin,self).generate_base()


    # Custom Section
    @api.model
    def _get_custom_barcode(self, item):
        """
        If the pattern is '23.....{NNNDD}'
        this function will return '23.....00000'
        Note : Overload _get_replacement_char to have another char
        instead that replace 'N' and 'D' char.
        """
        if item._name =='product.product':
            if not item.product_tmpl_id.barcode_rule_id and not item.categ_id.barcode_rule_id:
                return False

            # Define barcode
            custom_code = item.barcode_rule_id.pattern
            custom_code = custom_code.replace('{', '').replace('}', '')
            custom_code = custom_code.replace(
                'D', self._get_replacement_char('D'))
            return custom_code.replace(
                'N', self._get_replacement_char('N'))
        else:
            super(BarcodeGenerateMixin,self)._get_custom_barcode(item)

