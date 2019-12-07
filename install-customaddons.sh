#!/bin/bash
# -*- encoding: utf-8 -*-

OE_VER="12"
OE_USER="odoo"
OE_HOME="/opt/$OE_USER"
OE_HOMEV="/opt/$OE_USER/v$OE_VER"
OE_HOME_EXT="$OE_HOMEV/$OE_USER-server"
OE_VERSION=$OE_VER".0"

echo -e "\n---- : ----"

sudo su $OE_USER -c "mkdir -p -v $OE_HOMEV/repos"
sudo su $OE_USER -c "mkdir -p -v $OE_HOMEV/addons"
cd $OE_HOMEV/repos

git clone -b $OE_VERSION https://github.com/aaltinisik/access-addons
git clone -b $OE_VERSION https://github.com/aaltinisik/account-financial-tools
git clone -b $OE_VERSION https://github.com/aaltinisik/account-invoicing.git
git clone -b $OE_VERSION https://github.com/aaltinisik/account-payment.git
git clone -b $OE_VERSION https://github.com/aaltinisik/connector-telephony.git
git clone -b $OE_VERSION https://github.com/aaltinisik/crm
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
git clone -b $OE_VERSION https://github.com/aaltinisik/odoomrp-wip.git
git clone -b $OE_VERSION https://github.com/aaltinisik/mail-addons.git
git clone -b $OE_VERSION https://github.com/aaltinisik/stock-logistics-barcode.git
git clone -b $OE_VERSION https://github.com/aaltinisik/techspawn-odoo-apps.git


echo -e "\n---- Setting permissions on home folder ----"
sudo chown -R $OE_USER:$OE_USER $OE_HOME/*

while true; do
    read -p "Would you like to symlink selected modules to custom/addons folder  (y/n)?" yn
    case $yn in
        [Yy]* ) cd $OE_HOME






        break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

