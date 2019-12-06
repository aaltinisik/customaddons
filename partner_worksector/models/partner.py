# -*- coding: utf-8 -*-

from odoo import models,fields,api

class PartnerWorksector(models.Model):
    _name = 'partner.worksector'
    _description="Work Sector"

    
    description =  fields.Text(string="Description", translate=True)
    name = fields.Char(string="Name", translate=True)
    partner_ids = fields.Many2many('res.partner', 'table_worksector_partner_rel', 'wid', 'partid', string="Partner")
    product_categ_ids = fields.Many2many('product.category', string="Category")


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.depends()
    def _compute_product_categ(self):
        for part in self:
            lst = []
            for line in part.worksector_ids:
                lst += [x.id for x in line.product_categ_ids]
            part.target_product_categ_ids = self.env['product.category'].browse(set(lst))

    worksector_ids=fields.Many2many('partner.worksector', 'table_worksector_partner_rel', 'partid', 'wid', string="Worksector")
    target_product_categ_ids=fields.Many2many('product.category', string="Target Product Category",compute="_compute_product_categ")
