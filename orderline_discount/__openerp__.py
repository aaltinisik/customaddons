
{
    'name': 'Order Line Discount',
    'version': '8.0.2',
    'website': 'https://www.odoo.com',
    'category': 'Sales',
    'summary': 'Sale Order Line Discount',
    'description': """
	 """,
    'depends': [
        'sale', 'product_visible_discount'
    ],
    'data': [
            'wizard/update_discount_view.xml',
            'views/sale_order_view.xml',
    ],
    'installable' : True,
    'auto_install' : False,
}
