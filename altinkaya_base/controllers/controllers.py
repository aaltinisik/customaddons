# -*- coding: utf-8 -*-
from odoo import http

# class AltinkayaBase(http.Controller):
#     @http.route('/altinkaya_base/altinkaya_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/altinkaya_base/altinkaya_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('altinkaya_base.listing', {
#             'root': '/altinkaya_base/altinkaya_base',
#             'objects': http.request.env['altinkaya_base.altinkaya_base'].search([]),
#         })

#     @http.route('/altinkaya_base/altinkaya_base/objects/<model("altinkaya_base.altinkaya_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('altinkaya_base.object', {
#             'object': obj
#         })