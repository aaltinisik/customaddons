# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2012-Present (<http://www.acespritech.com/>) Acespritech Solutions Pvt.Ltd
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, api, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def open_sales_order(self):
        self.ensure_one()
        action = self.env.ref('sale.action_orders').read()[0]
        form = self.env.ref('sale.view_order_form')
        action['views'] = [(form.id, 'form')]
        action['res_id'] = self.sale_id.id
        return action

    x_durum = fields.Selection(
        [('1', u'İthal Eksik'),
         ('2', u'CNC Kesimde'),
         ('3', u'Enjeksiyonda'),
         ('4', u'Montajda'),
         ('5', u'Çıkacak'),
         ('6', u'ACİL'),
         ('7', u'Müsteriyi Bekliyor'),
         ('8', u'Profil Kesimde'),
         ('9', u'Sac Üretiminde'),
         ('A', u'Boyada'),
         ('B', u'Piyasadan Teminde')
         ],
        'Durumu', index=True)
    x_hazirlayan = fields.Selection(
        [("Asim", u"Asım"),
         ("Muhammet", u"Muhammet"),
         ("Harun", u"Harun"),
         ("Bilal", u"Bilal"),
         ("Saffet", u"Saffet"),
         ("Esra", u"Esra"),
         ("Selma", u"Selma"),
         (u"Uğur", u"Uğur"),
         (u"Çağrı", u"Çağrı"),
         ("Hatice", u"Hatice"),
         ("Muhsin", u"Muhsin"),
         ("Muharrem", u"Muharrem"),
         ("Sefer", "Sefer")
         ],
        u'Siparişi Hazırlayan', readonly=True)
    comment_irsaliye = fields.Text('İrsaliye Notu')
    hazirlayan = fields.Many2one('hr.employee', 'Sevki Hazırlayan')
    teslim_alan = fields.Char('Malı Teslim Alan', size=32)
    country_id = fields.Many2one('res.country',
                                 string='Country',
                                 related='partner_id.country_id',
                                 store=True,
                                 )
    partner_invoice_id = fields.Many2one('res.partner',
                                         string='Invoice Address',
                                         related='sale_id.partner_invoice_id',
                                         store=True,
                                         )
    sales_uid = fields.Many2one('res.users',
                                string='Sales Person',
                                related='sale_id.create_uid',
                                store=True,
                                )
    sale_note = fields.Text('Sale Note', related='sale_id.note', readonly=True)
    trimmed_sale_note = fields.Text('Sale Note', compute='_compute_trimmed_sale_note', readonly=True, store=False)

    @api.onchange('carrier_id')
    def _onchange_carrier_id(self):
        source = self.sale_id or self.purchase_id
        if self.carrier_id and source:
            source.write({'carrier_id': self.carrier_id.id})

    def force_assign(self):
        for pick in self:
            move_ids = [x for x in pick.move_lines if x.state in ['confirmed', 'waiting']]
            self.env['stock.move'].force_assign(moves=move_ids)
            pick.button_validate()
        return True

    @api.depends('sale_id.note')
    def _compute_trimmed_sale_note(self):
        """
        Trims the sale note to the first 50 characters.
        """
        for pick in self:
            if pick.sale_id.note and len(pick.sale_id.note) > 50:
                pick.trimmed_sale_note = pick.sale_id.note[:50] + "..."
            else:
                pick.trimmed_sale_note = pick.sale_id.note

    @api.multi
    def open_record(self):
        form_id = self.env.ref('stock.view_picking_form')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_id.id,
            'context': {},
            'target': 'current',
        }
