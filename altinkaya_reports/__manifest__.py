{
    'name' : 'Altinkaya Reports',
    'version' : '12.0',
    'category': 'General',
    'depends' : ['base','contacts', 'sale', 'stock','l10n_tr_invoice_amount_in_words','base_report_to_printer','account','account_check','mrp'],
    'author' : 'OnurUgur,Codequarters,',
    'description': """
    Contain altinkaya reports"
    """,
    'website': 'http://www.codequarters.com',
    'data': [
             'data/partner_data.xml',
             'report/sale_reports.xml',
             'report/paperformat.xml',
             'report/purchase_quotation_reports.xml',
             'report/purchase_order_reports.xml',
             'report/location_reports.xml',
             'report/report_mrp_production.xml',
             'report/stock_picking_report.xml',
             'report/report_account_payment.xml',
             'report/report_list_mrp.xml',
             'report/report_stock_delivery_carrier.xml',
             'report/report_hr_employee_annual.xml',
             'report/stock_picking_delivery.xml',
             'report/partner_statement.xml',
             'report/partner_statement2.xml',
             'views/res_users_views.xml',
             'views/partner_view.xml',
             'wizard/partner_statement_wizard_view.xml',
             'report/reports.xml',
             
            ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    
}