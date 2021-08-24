# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2012-Present (<http://www.acespritech.com/>) Acespritech Solutions Pvt.Ltd
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
    'name' : 'Altinkaya Sale Order Extensions',
    'version' : '12.0',
    'category': 'General',
    'depends' : ['base', 'sale', 'stock', 'sale_stock', 'delivery', 'partner_fax', 'altinkaya_roles', 'altinkaya_mrp'],
    'author' : 'MAkifOzdemir,Codequarters,Acespritech Solutions Pvt. Ltd.',
    'description': """
    Sales Order Customization
    """,
    'website': 'http://www.codequarters.com',
    'data': [
             'security/ir.model.access.csv',
             'views/sale_workflow_new_menus_actions.xml',
             'views/sales_order_view.xml',
             'views/res_partner_views.xml',
             'views/product_views.xml',
             'views/pricelist.xml',
             "views/res_partner.xml",
             "data/mail_data.xml"
            ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    
}
