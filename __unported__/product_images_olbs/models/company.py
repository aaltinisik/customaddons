# -*- encoding: utf-8 -*-
##############################################################################
#
#    Author Nicolas Bessi & Guewen Baconnier. Copyright Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api,_

class ResCompany(models.Model):
    """Override company to add images configuration"""
    _inherit = "res.company"
         
    local_media_repository = fields.Char(
                    'Images Repository Path', 
                    size=256, 
                    help='Local mounted path on OpenERP server where all your images are stored.'
                )
   
    
    @api.multi
    def get_local_media_repository(self):
        if self.id:
            return self.local_media_repository
#         user_obj = self.env['res.users'].browse(self.end.uid)
        commp = self.search([])
        print ("commp", commp)
        return commp[0].local_media_repository


