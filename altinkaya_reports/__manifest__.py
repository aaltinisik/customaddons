{
    'name' : 'Altinkaya Reports',
    'version' : '12.0',
    'category': 'General',
    'depends' : ['base', 'sale', 'stock','l10n_tr_invoice_amount_in_words','base_report_to_printer','account','account_check','mrp'],
    'author' : 'OnurUgur,Codequarters,',
    'description': """
    Contain altinkaya reports"
    """,
    'website': 'http://www.codequarters.com',
    'data': [
              'report/sale_reports.xml',
             'report/paperformat.xml',
             'report/purchase_quotation_reports.xml',
             'report/purchase_order_reports.xml',
             'report/location_reports.xml',
             'report/report_mrp_production.xml',
             'report/stock_picking_report.xml',
             'report/reports.xml',
             'report/report_account_payment.xml',
             'report/report_list_mrp.xml',
             'report/report_stock_delivery_carrier.xml',
             'views/res_users_views.xml',
             
            ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    
}