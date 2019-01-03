#!/bin/bash
# -*- encoding: utf-8 -*-

##fixed parameters
#openerp

OE_USER="odoo"
OE_HOME="/opt/$OE_USER"
OCA_HOME="/opt/odoo/12/repos"
OE_HOME_EXT="/opt/$OE_USER/$OE_USER12"
# Replace for openerp-gevent for enabling gevent mode for chat
OE_SERVERTYPE="openerp-server"
OE_VERSION="12.0"
#set the superadmin password
OE_CONFIG="odoo-server"

echo -e "\n---- : ----"
cd $OE_HOME
mkdir $OE_HOME/12
cd $OE_HOME/12
mkdir $OE_HOME/12/addons
mkdir $OE_HOME/12/repos
cd $OE_HOME/12/repos

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
git clone -b $OE_VERSION https://github.com/aaltinisik/techspawn-odoo-apps.git




while true; do
    read -p "Would you like to symlink selected modules to custom/addons folder  (y/n)?" yn
    case $yn in
        [Yy]* ) cd $OE_HOME






        break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

