# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    'name': 'Web Key Shortcut',
    'category': 'Web',
    'description':"""
        Module to add keyboard shotcut to OpenERP web
    """,
    'author': 'Zesty Beanz Technologies',
    'website': 'http://www.zbeanztech.com/',
    'version': '1.0',
    'depends': ['base','web'],
    'data': [
             'web_shortcut_view.xml',
             'security/web_key_user_security.xml',
             'security/ir.model.access.csv'
             ],
    'js': [
           'static/src/js/web_shortcut.js'
           ],
    'qweb' : [
              'static/src/xml/web_shortcut.xml'
              ],
    'css': [
            'static/src/css/web_shortcut.css'
            ],
    'auto_install': False,
    'web_preload': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: