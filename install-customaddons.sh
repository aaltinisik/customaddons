#!/bin/bash
# -*- encoding: utf-8 -*-

##fixed parameters
#openerp

OE_USER="odoo"
OE_HOME="/opt/$OE_USER"
OCA_HOME="/opt/odoo/custom/repos"
OE_HOME_EXT="/opt/$OE_USER/$OE_USER-server"
# Replace for openerp-gevent for enabling gevent mode for chat
OE_SERVERTYPE="openerp-server"
OE_VERSION="8.0"
#set the superadmin password
OE_CONFIG="odoo-server"

echo -e "\n---- : ----"
cd $OE_HOME
mkdir $OE_HOME/custom
cd $OE_HOME/custom
mkdir $OE_HOME/custom/addons
mkdir $OE_HOME/custom/repos
cd $OE_HOME/custom/repos

git clone -b $OE_VERSION https://github.com/aaltinisik/access-addons
git clone -b $OE_VERSION https://github.com/aaltinisik/account-financial-tools
git clone -b $OE_VERSION https://github.com/aaltinisik/account-invoicing.git
git clone -b $OE_VERSION https://github.com/aaltinisik/account-payment.git
git clone -b $OE_VERSION https://github.com/aaltinisik/addons-onestein
git clone -b $OE_VERSION https://github.com/aaltinisik/aeroo_reports
git clone -b $OE_VERSION https://github.com/aaltinisik/bank-statement-import.git
git clone -b $OE_VERSION https://github.com/aaltinisik/connector-telephony.git
git clone -b $OE_VERSION https://github.com/aaltinisik/crm
git clone -b $OE_VERSION https://github.com/aaltinisik/gant_improvement
git clone -b $OE_VERSION https://github.com/aaltinisik/geospatial.git
git clone -b $OE_VERSION https://github.com/aaltinisik/knowledge.git
git clone -b $OE_VERSION https://github.com/aaltinisik/misc-addons.git
git clone -b $OE_VERSION https://github.com/aaltinisik/partner-contact.git
git clone -b $OE_VERSION https://github.com/aaltinisik/product-attribute.git
git clone -b $OE_VERSION https://github.com/aaltinisik/purchase-workflow.git
git clone -b $OE_VERSION https://github.com/aaltinisik/reporting-engine
git clone -b $OE_VERSION https://github.com/aaltinisik/report-print-send.git
git clone -b $OE_VERSION https://github.com/aaltinisik/sale-workflow
git clone -b $OE_VERSION https://github.com/aaltinisik/server-tools.git
git clone -b $OE_VERSION https://github.com/aaltinisik/stock-logistics-tracking.git
git clone -b $OE_VERSION https://github.com/aaltinisik/stock-logistics-warehouse
git clone -b $OE_VERSION https://github.com/aaltinisik/stock-logistics-workflow
git clone -b $OE_VERSION https://github.com/aaltinisik/web.git
git clone -b $OE_VERSION https://github.com/aaltinisik/CybroAddons.git
git clone -b $OE_VERSION https://github.com/aaltinisik/addons-vauxoo.git
git clone -b $OE_VERSION https://github.com/aaltinisik/SerpentCS_Contributions.git
git clone -b $OE_VERSION https://github.com/aaltinisik/stock-logistics-reporting.git
git clone -b $OE_VERSION https://github.com/aaltinisik/manufacture.git
git clone -b $OE_VERSION https://github.com/aaltinisik/odoomrp-utils.git
git clone -b $OE_VERSION https://github.com/aaltinisik/odoomrp-wip.git
git clone -b $OE_VERSION https://github.com/aaltinisik/mail-addons.git
git clone -b $OE_VERSION https://github.com/aaltinisik/stock-logistics-barcode.git




while true; do
    read -p "Would you like to symlink selected modules to custom/addons folder  (y/n)?" yn
    case $yn in
        [Yy]* ) cd $OE_HOME




ln -s -f $OCA_HOME/bank-statement-import/account_bank_statement_import $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/bank-statement-import/account_bank_statement_import_camt $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/account-payment/account_due_list_days_overdue $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/account-invoicing/account_invoice_merge $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/account-invoicing/account_invoice_partner $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/admin_technical_features $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/connector-telephony/asterisk_click2dial $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/connector-telephony/asterisk_click2dial_crm $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/knowledge/attachment_preview $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/knowledge/attachments_to_filesystem $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/auth_admin_passkey $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/base_concurrency $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/base_export_manager $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/base_name_search_improved $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/base_optional_quick_create $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/auditlog $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/auto_backup $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/base_import_match $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/base_import_security_group $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/access-addons/ir_rule_protected $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/addons-vauxoo/mrp_production_procurement_order $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/addons-vauxoo/mrp_production_security_force $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/addons-vauxoo/mrp_workcenter_responsible $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/addons-vauxoo/product_available_by_warehouse $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/knowledge/attachments_to_filesystem $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/manufacture/mrp_hook $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/manufacture/mrp_operations_extension $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/manufacture/mrp_sale_info $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/misc-addons/product_image_filestore $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/odoomrp-utils/product_packaging_views $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/odoomrp-utils/product_stock_info $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/odoomrp-utils/product_variant_default_code $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/odoomrp-utils/purchase_stock_quant_shortcut $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/odoomrp-utils/stock_quants_shortcuts $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/odoomrp-wip/product_variants_no_automatic_creation $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/odoomrp-wip/product_variants_types $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/odoomrp-wip/sale_product_variants $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/odoomrp-wip/stock_inventory_import $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/odoomrp-utils/mrp_show_related_attachment $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/odoomrp-utils/mrp_stock_quant_shortcut $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/odoomrp-utils/product_category_in_header $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/odoomrp-wip/product_packaging_through_attributes $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/product-attribute/product_attribute_priority $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/product-attribute/product_attribute_types $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/product-attribute/purchase_order_line_stock_available $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/reporting-engine/report_custom_filename $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-reporting/stock_analysis $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-warehouse/stock_inventory_line_price $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-warehouse/stock_inventory_preparation_filter $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-warehouse/stock_orderpoint_generator $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-warehouse/stock_orderpoint_manual_procurement $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-warehouse/stock_orderpoint_uom $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-workflow/stock_split_picking $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/addons-vauxoo/mrp_production_bom_related $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_offline_warning $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/connector-telephony/base_phone $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/connector-telephony/base_phone_popup $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/base_report_auto_create_qweb $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/report-print-send/base_report_to_printer $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/base_user_role $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/partner-contact/base_vat_sanitized $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/addons-onestein/bi_view_editor $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/connector-telephony/crm_claim_phone $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/connector-telephony/crm_phone $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/cron_run_manually $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/account-financial-tools/currency_rate_date_check $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/account-financial-tools/currency_rate_update $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/disable_openerp_online $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/connector-telephony/event_phone $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/CybroAddons/export_stockinfo_xls $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/fetchmail_notify_error_to_sender $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/gant_improvement/gantt_improvement $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/connector-telephony/hr_phone $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/connector-telephony/hr_recruitment_phone $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/inactive_session_timeout $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/access-addons/ir_rule_protected $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/language_path_mixin $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/crm/lettermgmt $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/connector-telephony/LICENSE $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/log_forwarded_for_ip $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/mass_editing $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/module_prototyper $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/partner-contact/partner_address_street3 $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/partner-contact/partner_external_maps $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/partner-contact/partner_financial_risk $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/sale-workflow/partner_prepayment $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/password_security $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/purchase-workflow/product_by_supplier $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/product-attribute/product_dimension $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/product-attribute/product_weight $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/purchase-workflow/purchase_order_revision $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/qweb_usertime $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/aeroo_reports/README.md $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/aeroo_reports/report_aeroo $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/aeroo_reports/report_aeroo_controller $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/aeroo_reports/report_aeroo_direct_print $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/aeroo_reports/report_aeroo_printscreen $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/aeroo_reports/report_aeroo_sample $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/reporting-engine/report_xlsx $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/sale-workflow/sale_automatic_workflow $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/sale-workflow/sale_cancel_reason $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/sale-workflow/sale_exceptions $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/sale-workflow/sale_order_add_variants $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/sale-workflow/sale_order_back2draft $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/sale-workflow/sale_order_price_recalculation $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/sale-workflow/sale_order_revision $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/sale-workflow/sale_order_unified_menu $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/sale-workflow/sale_packaging_price $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/sale-workflow/sale_partner_incoterm $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/sale-workflow/sale_payment_method $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/sale-workflow/sale_quick_payment $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/sale-workflow/sale_validity $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/save_translation_file $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/scheduler_error_mailer $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/secure_uninstall $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/security_protector $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-tracking/stock_barcode_reader $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-warehouse/stock_orderpoint_creator $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-warehouse/stock_orderpoint_manual_procurement $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-warehouse/stock_orderpoint_uom $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-tracking/stock_packaging_usability $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-tracking/stock_packaging_usability_ul $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-workflow/stock_picking_mass_action $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-workflow/stock_picking_package_preparation $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-warehouse/stock_quant_merge $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/server-tools/super_calendar $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_environment_ribbon $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_graph_improved $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_graph_sort $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_group_expand $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_hideleftmenu $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_last_viewed_records $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_listview_custom_element_number $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_offline_warning $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_recipients_uncheck $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_searchbar_full_width $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_sheet_full_width $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_translate_dialog $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_tree_image $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_widget_image_download $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/web_widget_many2many_tags_multi_selection $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/product-attribute/product_attribute_types $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/product-attribute/product_attribute_types_views $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-barcode/product_barcode_generator $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-barcode/product_multi_ean $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/odoomrp-wip/product_variant_default_code $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/odoomrp-utils/purchase_order_line_stock_available $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/stock-logistics-barcode/stock_inventory_barcode $OE_HOME/custom/addons/
ln -s -f $OCA_HOME/web/support_branding $OE_HOME/custom/addons/

        break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

