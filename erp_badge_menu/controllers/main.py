# -*- coding: utf-8 -*-
import json
import base64
import logging

from odoo import api, fields, models, tools, _
from odoo import http
from odoo.http import request
from datetime import datetime, time

_logger = logging.getLogger(__name__)


class UploadAttachment(http.Controller):
    def find_notification_by_menu(self, menu, models):
        count = 0
        model_fount = []
        for m in models:
            model_fount.append(m)
        if menu.action.type == 'ir.actions.act_window' and menu.action.res_model not in model_fount:
            model_id = request.env['ir.model'].search([("model", "=", menu.action.res_model)])
            model_fount.append(menu.action.res_model)
            if model_id:
                activities = request.env['mail.activity'].search([("res_model_id", "=", model_id.id),
                    ("date_deadline", "<=", datetime.now().date())])
                if activities:
                    count = len(activities)

                #show count here for each model
                #if model_id.model=='business.requirement':
                #    count = (request.env['business.requirement'].search_count([]))
        return (count, model_fount)

    @http.route(['/get_badge_count'], type='http', auth='user', website=True)
    def get_badge_count(self,  **post):
        menu_id = post.get("menu_id")
        all_menu = request.env['ir.ui.menu'].search([('id','=',menu_id)])
        notification_count = self.find_notification_by_menu(all_menu,[])[0]
        return json.dumps({'count': notification_count})
