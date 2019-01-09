# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    This module copyright (C) 2017 Ahmet Altinisik#    (https://www.altinkaya.com.tr).#
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
    'name': 'Warehouse Filters',
    'version': '8.0.1.0.0',
    'author': 'Ahmet Altinisik',
    'maintainer': 'Altınkaya',
    'website': 'https://www.altinkaya.com.tr',
    'license': '',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml # noqa
    # for the full list
    'category': 'stock',    'summary': 'Altinkaya Warehouse Filtreleri',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
Warehouse Filters
==============

Adding new views and search filters to warehouse views.

Installation
============

To install this module, you need to:

 * install it



Credits
=======

Contributors
------------

* Ahmet Altinisik <aaltinisik@altinkaya.com.tr>

""",

    # any module necessary for this one to work correctly
    'depends': [
            'stock',
    ],
    'external_dependencies': {
        'python': [],
    },

    # always loaded
    'data': [
            'views/stock_picking_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],

    # used for Javascript Web CLient Testing with QUnit / PhantomJS
    # https://www.odoo.com/documentation/8.0/reference/javascript.html#testing-in-odoo-web-client  # noqa
    'js': [],
    'css': [],
    'qweb': [],

    'installable': True,

    'auto_install': False,
    'application': False,
}
