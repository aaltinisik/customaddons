# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Intero Technologies GmbH
#                                (<http://intero-technologies.de>).
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
{
    "name": "Reload Button",
    "version": "1.0.0",
    "author": "Intero Technologies GmbH",
    "category": "View",
    'summary': """Reload Form Records without entering a number""",
    "description": """
    adds a reload button to the form view.
    EE only.
    """,
    "depends": ["base", "web"],
    "data": ["views/assets.xml",
             
             ],
    'qweb' : [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'images':['static/description/store_img_cover.png'],
    'website': 'https://www.intero-technologies.de',
    'Read description for':[]

}
