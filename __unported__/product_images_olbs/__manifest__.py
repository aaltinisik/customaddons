# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
#    Copyright (C) 2009  Sharoon Thomas, Open Labs Business solutions        #
#                                                                            #
#    This program is free software: you can redistribute it and/or modify    #
#    it under the terms of the GNU Affero General Public License as          #
#    published by the Free Software Foundation, either version 3 of the      #
#    License, or (at your option) any later version.                         #
#                                                                            #
#    This program is distributed in the hope that it will be useful,         #  
#    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#    GNU Affero General Public License for more details.                     #
#                                                                            #
#                                                                            #
##############################################################################

{
    "name" : "Product Image Gallery",
    "version" : "0.1 ",
    "author" : "Sharoon Thomas, Open Labs Business Solutions",
    "website" : "http://openlabs.co.in/",
    "category" : "Added functionality - Product Extension",
    "depends" : ['base','product'],
    "description": """
    This Module implements an Image Gallery for products.
    You can add images against every product.
    
    This module is generic but built for Magento ERP connector and
    the upcoming e-commerce system for Open ERP by Open Labs
    """,
    "init_xml": [],
    "data": [
        'security/ir.model.access.csv',
        'views/product_images_view.xml',
        'views/company_view.xml'
    ],
    "installable": True,
    "active": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
