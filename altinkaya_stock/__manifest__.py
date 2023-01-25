{
    'name': 'Altinkaya Stock',
    'version': '12.0',
    'website': 'https://www.altinkaya.com.tr',
    'author':'Ahmet Altınışık,OnurUgur,Codequarters,Yavuz Avcı',
    'category': 'Stock',
    'summary': 'add specialized stock extensions',
    'description': """
     """,
    'depends': [
        'stock','delivery', 'delivery_integration_base'
    ],
    'data': [
        'views/stock_quant_view.xml',
        'views/stock_picking_views.xml',
        'views/stock_view.xml',
        'views/stock_location_view.xml',
        'views/stock_location_route_views.xml',
        'views/stock_rule_views.xml',
        'views/sale_view.xml',
        'views/product_views.xml',
        'views/delivery_carrier_views.xml',
        'wizard/wizard_create_procurement_move.xml',
        'wizard/wizard_make_mts_move.xml',
        'wizard/wizard_update_unreserved_quants.xml',
        'views/stock_warehouse_orderpoint_view.xml',
        'views/mrp_production_view.xml',
        "security/security_group.xml",
    ],
    'installable': True,
    'auto_install': False,
}
