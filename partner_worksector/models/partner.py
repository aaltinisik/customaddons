# -*- coding: utf-8 -*-

from odoo import models,fields,api

class PartnerWorksector(models.Model):
    _name = 'partner.worksector'
    _description="Work Sector"

    
    description =  fields.Text(string="Description", translate=True)

    code = fields.Char(string="USSIC Code", translate=False, size=8, description="USSIC Code consists of 8 digits number")
    name = fields.Char(string="US SIC Description", translate=True)
    partner_ids = fields.Many2many('res.partner', 'table_worksector_partner_rel', 'wid', 'partid', string="Partner")
    product_categ_ids = fields.Many2many('product.category', string="Category")
    UKSIC_code = fields.Char(string="UKSIC Code")
    UKSIC_name = fields.Char(string="UKSIC Name", translate=True)
    EUNACE_code = fields.Char(string="EUNACE Code")
    EUNACE_name = fields.Char(string="EUNACE Name", translate=True)

    _order = 'code, id desc'

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for sector in self:
            if sector.code:
                name = sector.code + ' - ' + sector.name
            else:
                name = sector.name
            result.append((sector.id, name))
        return result



class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.depends()
    def _compute_product_categ(self):
        for partner in self:
            lst = []
            if partner.main_worksector_id:
                lst.append(partner.main_worksector_id.product_categ_ids)
            for line in partner.worksector_ids:
                lst += [x.id for x in line.product_categ_ids]
            partner.target_product_categ_ids = self.env['product.category'].browse(set(lst))

    main_worksector_id = fields.Many2one('partner.worksector', string="Main Worksector",ondelete='restrict')
    worksector_ids=fields.Many2many('partner.worksector', 'table_worksector_partner_rel', 'partid', 'wid', string="Worksector")
    target_product_categ_ids=fields.Many2many('product.category', string="Target Product Category",compute="_compute_product_categ")

