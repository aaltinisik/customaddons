# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    This module copyright (C) 2017 Ahmet Altinisik#    (http://www.altinkaya.com.tr).#
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
    'name': 'Altinkaya Shipment',
    'version': '8.0.1.0.0',
    'author': 'Ahmet Altinisik,Kiran',
    'maintainer': 'False',
    'website': 'http://www.altinkaya.com.tr',
    'license': '',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml # noqa
    # for the full list
    'category': 'False',    'summary': 'Shipment customizations for Altinkaya',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========
Module name
===========

This module written to add addtional functionaltiy for Shipment calculations

Installation
============

To install this module, you need to:

 * do this ...

Configuration
=============

To configure this module, you need to:

 * go to ...

Usage
=====

To use this module, you need to:

 * go to ...



Known issues / Roadmap
======================

 * ...

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/{project_repo}/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/{project_repo}/issues/new?body=module:%20{module_name}%0Aversion:%20{version}%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Ahmet Altinisik <aaltinisik@altinkaya.com.tr>



* Module exported by the Module Prototyper module for version 8.0.
* If you have any questions, please contact Savoir-faire Linux
(support@savoirfairelinux.com)
""",

    # any module necessary for this one to work correctly
    'depends': [
            'sale',
            'stock',
    ],
    'external_dependencies': {
        'python': [],
    },

    # always loaded
    'data': [
            'views/product_product_view.xml',
            'views/product_template_view.xml',
            'views/product_template_menus.xml',
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
    # Install this module automatically if all dependency have been previously
    # and independently installed.  Used for synergetic or glue modules.
    'auto_install': False,
    'application': False,
}
