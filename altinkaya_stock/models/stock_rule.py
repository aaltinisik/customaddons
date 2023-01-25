# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields


class StockRuleInherit(models.Model):
    _name = "stock.rule"
    _inherit = ["mail.thread", "stock.rule"]

    # Add tracking to the field
    action = fields.Selection(track_visibility="onchange")
    picking_type_id = fields.Many2one(track_visibility="onchange")
    location_src_id = fields.Many2one(track_visibility="onchange")
    location_id = fields.Many2one(track_visibility="onchange")
    route_id = fields.Many2one(track_visibility="onchange")
    auto = fields.Selection(track_visibility="onchange")
    sequence = fields.Integer(track_visibility="onchange")
    warehouse_id = fields.Many2one(track_visibility="onchange")
    propagate_warehouse_id = fields.Many2one(track_visibility="onchange")
    group_propagation_option = fields.Selection(track_visibility="onchange")
    mts_rule_id = fields.Many2one(track_visibility="onchange")
    mts2_rule_id = fields.Many2one(track_visibility="onchange")
    mto_rule_id = fields.Many2one(track_visibility="onchange")
    do_not_split_percentage = fields.Float(track_visibility="onchange")
