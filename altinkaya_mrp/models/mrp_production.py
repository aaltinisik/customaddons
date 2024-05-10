# Copyright 2024 Yousef Sheta (https://github.com/TrueYouface)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api, _


class MrpProduction(models.Model):
    _inherit = "mrp.production"


    # TODO: add field "routing_id" when possible

    mo_printed = fields.Boolean("Manufacting Order Printed", default=False)
    sale_id = fields.Many2one("sale.order", string="Sale Order")
    # sale_note = fields.Text("Sale Note", related="sale_id.note", readonly=True)
    active_rule_id = fields.Many2one("stock.rule", string="Active Rule")
    date_planned = fields.Datetime("Scheduled Date")
    date_start2 = fields.Datetime("Start Date")
    date_finished2 = fields.Datetime("End Date")
    priority = fields.Selection(
        [("0", "Not urgent"), ("1", "Normal"), ("2", "Urgent"), ("3", "Very Urgent")],
        string="Priority",
        default="0",
    )


    process_id = fields.Many2one(
        "mrp.routing",
        string="Rota",
        readonly=True,
        # related="bom_id.routing_id",
        store=True,
    )
    availability = fields.Selection([
        ('assigned', 'Available'),
        ('partially_available', 'Partially Available'),
        ('waiting', 'Waiting'),
        ('none', 'None')], string='Materials Availability',
        # compute='_compute_availability',
        store=True)