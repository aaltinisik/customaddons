# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models


class IrBinary(models.AbstractModel):
    _inherit = "ir.binary"

    def _find_record(
        self,
        xmlid=None,
        res_model="ir.attachment",
        res_id=None,
        access_token=None,
    ):
        """
        Override this method to allow access to product.template attachments with
        public user.
        """
        record = super()._find_record(xmlid, res_model, res_id, access_token)
        srecord = record.sudo()

        if res_model == "ir.attachment" and srecord.res_model == "product.template":
            tmpl_id = self.env["product.template"].browse(srecord.res_id)

            if tmpl_id and (srecord.id in tmpl_id.website_attachment_ids.ids):
                record = srecord

        return record
