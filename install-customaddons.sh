#!/bin/bash
# -*- encoding: utf-8 -*-

##fixed parameters
#openerp

OE_DATABASE="upgrade1"
OE_USER="odoo"
OE_HOME="/opt/$OE_USER"
OCA_HOME="/opt/odoo/OCA"
OE_HOME_EXT="/opt/$OE_USER/$OE_USER-server"
# Replace for openerp-gevent for enabling gevent mode for chat
OE_SERVERTYPE="openerp-server"
OE_VERSION="8.0"
#set the superadmin password
OE_CONFIG="odoo-server"


# Install Aeroo Reports:
echo -e "\n---- Install community   Modules: ----"

while true; do
    read -p "Would you like to clone git repos of community modules (y/n)?" yn
    case $yn in
        [Yy]* ) cd $OE_HOME
        git clone -b 8.0 https://github.com/aaltinisik/customaddons.git $OE_HOME/customaddons
        mkdir $OCA_HOME
        cd $OCA_HOME
        git clone -b 8.0 https://github.com/aaltinisik/aeroo_reports $OCA_HOME/aeroo_reports
        git clone -b 8.0 https://github.com/aaltinisik/connector-telephony.git $OCA_HOME/connector-telephony    
        git clone -b 8.0 https://github.com/OCA/web.git $OCA_HOME/web
        git clone -b 8.0 https://github.com/yelizariev/addons-yelizariev.git $OCA_HOME/addons-yelizariev
        git clone -b 8.0 https://github.com/OCA/server-tools.git $OCA_HOME/server-tools
        git clone -b 8.0 https://github.com/OCA/knowledge.git $OCA_HOME/knowledge
        git clone -b 8.0 https://github.com/OCA/purchase-workflow.git $OCA_HOME/purchase-workflow
        git clone -b 8.0 https://github.com/OCA/product-attribute.git $OCA_HOME/product-attribute
        git clone -b 8.0 https://github.com/OCA/sale-workflow.git $OCA_HOME/sale-workflow
        git clone -b 8.0 https://github.com/OCA/account-invoicing.git $OCA_HOME/account-invoicing
        git clone -b 8.0 https://github.com/OCA/stock-logistics-tracking.git $OCA_HOME/stock-logistics-tracking
        git clone -b 8.0 https://github.com/OCA/partner-contact.git $OCA_HOME/partner-contact
       
        break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

while true; do
    read -p "Would you like to symlink selected modules to custom/addons folder  (y/n)?" yn
    case $yn in
        [Yy]* ) cd $OE_HOME
        ln -s -f $OCA_HOME/connector-telephony/* $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/aeroo_reports/* $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/aeroo_reports/* $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/web/web_widget_many2many_tags_multi_selection $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/web/web_translate_dialog $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/web/web_sheet_full_width $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/web/web_searchbar_full_width $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/web/web_last_viewed_records $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/server-tools/auth_admin_passkey $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/server-tools/base_concurrency $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/server-tools/cron_run_manually $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/web/web_environment_ribbon $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/server-tools/scheduler_error_mailer $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/server-tools/base_optional_quick_create $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/server-tools/base_report_auto_create_qweb $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/server-tools/disable_openerp_online $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/server-tools/fetchmail_notify_error_to_sender $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/server-tools/language_path_mixin $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/server-tools/module_prototyper $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/server-tools/mass_editing $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/server-tools/super_calendar $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/knowledge/attachment_preview $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/knowledge/attachments_to_filesystem $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/purchase-workflow/product_by_supplier $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/purchase-workflow/purchase_order_revision $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/partner-contact/partner_external_maps $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/product-attribute/product_dimension $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/product-attribute/product_weight $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/sale-workflow/partner_prepayment $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/sale-workflow/sale_automatic_workflow $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/sale-workflow/sale_cancel_reason $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/sale-workflow/sale_order_back2draft $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/sale-workflow/partner_prepayment $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/sale-workflow/sale_automatic_workflow $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/sale-workflow/sale_cancel_reason $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/sale-workflow/sale_order_back2draft $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/sale-workflow/sale_order_price_recalculation $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/sale-workflow/sale_order_revision $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/sale-workflow/sale_partner_incoterm $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/sale-workflow/sale_payment_method $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/sale-workflow/sale_validity $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/account-invoicing/account_invoice_partner $OE_HOME/custom/addons/
        ln -s -f $OCA_HOME/stock-logistics-tracking/stock_barcode_reader $OE_HOME/custom/addons/
    
        break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

