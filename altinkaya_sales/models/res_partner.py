"""
Created on Jan 16, 2019

@author: cq
"""

from odoo import models, fields, api
import logging


_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _search_nace_product_categ(self, operator, value):
        return [
            (
                "secondary_nace_ids.product_categ_ids",
                operator,
                value,
            )
        ]

    def _search_property_product_pricelist(self, operator, value):
        """
        Actually this is not a real property, but a computed field.
        It takes too long to search for all partners and then filter them.
        So we are searching for sale orders with the given pricelist.
        """
        so_list = self.env["sale.order"].search([("pricelist_id", operator, value)])
        return [("id", "in", so_list.mapped("partner_id").ids)]

    property_product_pricelist = fields.Many2one(
        search="_search_property_product_pricelist",
        company_dependent=True,
    )
    nace_product_categ_ids = fields.Many2many(
        search="_search_nace_product_categ",
    )
    z_old_tel = fields.Char("Eski Tel", size=64, required=False)
    z_old_fax = fields.Char("Eski Faks", size=64, required=False)
    z_old_cep = fields.Char("Eski Cep", size=64, required=False)
    z_contact_name = fields.Char("İlgili Kişi", size=64, required=False)
    z_tel_kampanya = fields.Boolean(
        "Kampanyalarda Aranmayacak",
        default=False,
        help="Seçili ise telefon kampanyalarında aranmayacak.",
    )
    z_kamp_2016A = fields.Boolean(
        "2016 Katalog için arandı",
        help="2016 Temmuz Katalog gönderme kampanyası icin arandi.",
    )
    z_kamp_2017A = fields.Boolean(
        "2017 Adres güncelleme için arandı",
        help="2017 Temmuz Adres günceleme için arandı.",
    )
    z_kat_postala = fields.Boolean(
        "Katalog Postala", help="Katalog Posta ile gönderilecek."
    )
    z_kat_postalandi = fields.Boolean(
        "Katalog Postalandi", help="Katalog Posta ile gönderildi."
    )
    z_kat_email = fields.Boolean(
        "Katalog E-mail", help="Katalog email ile gönderilecek."
    )
    v_cari_urun_count = fields.Integer(
        "Carinin Urunleri", compute="_compute_v_cari_urun_count"
    )
    x_vergino = fields.Char("Vergi No", size=64)
    # make country_id is required in res.partner
    country_id = fields.Many2one(required=True)
    segment_id = fields.Many2one(
        "res.partner.segment",
        string="Segment",
    )
    email_invalid = fields.Boolean(
        "Email Invalid",
        default=False,
        store=True,
        compute="_compute_email_invalid",
    )
    credit_insurance = fields.Boolean(
        "Credit Insurance",
        default=False,
    )
    credit_insurance_validity = fields.Date(
        "Credit Insurance Validity"
    )

    @api.depends(lambda x: x._get_depends_compute_risk_exception())
    def _compute_risk_exception(self):
        """
        Inherited from account_financial_risk to add credit_insurance_validity
        :return:
        """
        super()._compute_risk_exception()
        for rec in self:
            if rec.credit_insurance and rec.credit_insurance_validity < fields.Date.today():
                rec.risk_exception = True

    @api.multi
    @api.depends("email")
    def _compute_email_invalid(self):
        for rec in self:
            try:
                if rec.email:
                    is_invalid = not bool(rec.email_check(rec.email))
                else:
                    is_invalid = False
            except:
                is_invalid = True
            _logger.info("Email %s is invalid: %s" % (rec.email, is_invalid))
            rec.email_invalid = is_invalid

    def action_view_v_cari_urun(self):
        action = self.env.ref("stock.stock_product_normal_action").read()[0]
        action["domain"] = [
            ("v_cari_urun", "=", self.id),
        ]
        return action

    @api.multi
    def _compute_v_cari_urun_count(self):
        for rec in self:
            rec.v_cari_urun_count = self.env["product.product"].search_count(
                [
                    ("v_cari_urun", "=", rec.id),
                ]
            )
