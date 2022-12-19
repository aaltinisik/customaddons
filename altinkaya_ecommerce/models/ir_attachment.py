# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import fields, models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    usage = fields.Selection(
        selection=[
            ('general', 'General'),
            ('dxf', 'DXF'),
            ('pdf', 'PDF'),
            ('3d', '3D'),
            ('ip67', 'IP67'),
        ],
        string='Usage',
        default='general',
    )
