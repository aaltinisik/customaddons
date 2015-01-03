###############################################################################
#
#    web_action_request module for OpenERP
#    Copyright (C) 2014 AKRETION (<http://www.akretion.fr>)
#                         Alexis DE LATTRE <alexis.delattre@akretion.com>
#    Copyright (C) 2014 ANYBOX (<http://www.anybox.fr>)
#                         Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
#    web_notification is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License v3 or later
#    as published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    anybox_login_demo is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License v3 or later for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    v3 or later along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
{
    'name': 'Action request',
    'version': '1.0.0',
    'sequence': 150,
    'category': 'Anybox',
    'description': """

    """,
    'author': 'Anybox',
    'website': 'http://anybox.fr',
    'depends': [
        'web_longpolling',
    ],
    'data': [
        'setting.xml',
    ],
    'js': [
        'static/src/js/request.js',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
