#!/bin/bash
# -*- encoding: utf-8 -*-

OE_VER="12"
OE_USER="odoo"
OE_HOME="/opt/$OE_USER"
OE_HOMEV="/opt/$OE_USER/v$OE_VER"
OE_HOME_EXT="$OE_HOMEV/$OE_USER-server"
OE_VERSION=$OE_VER".0"

echo -e "\n---- : ----"

sudo pip3 install -r https://github.com/aaltinisik/customaddons/raw/${OE_VERSION}/requirements.txt
sudo su $OE_USER -c "mkdir -p -v $OE_HOMEV/repos"
sudo su $OE_USER -c "mkdir -p -v $OE_HOMEV/addons"
cd $OE_HOMEV/repos

git clone -b $OE_VERSION https://github.com/aaltinisik/access-addons
cd access-addons
git remote add upstream https://github.com/it-projects-llc/access-addons.git
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/account-financial-tools
cd account-financial-tools
git remote add upstream https://github.com/OCA/account-financial-tools.git
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/account-invoicing.git
cd account-invoicing 
git remote add upstream https://github.com/OCA/account-invoicing
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/account-payment.git
cd  account-payment
git remote add upstream https://github.com/OCA/account-payment
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/connector-telephony.git
cd  connector-telephony
git remote add upstream https://github.com/OCA/connector-telephony
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/crm
cd  crm
git remote add upstream https://github.com/OCA/crm
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/knowledge.git
cd  knowledge
git remote add upstream https://github.com/OCA/knowledge
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/misc-addons.git
cd  misc-addons
git remote add upstream https://github.com/it-projects-llc/misc-addons 
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/partner-contact.git
cd  partner-contact
git remote add upstream https://github.com/OCA/partner-contact
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/product-attribute.git
cd  product-attribute
git remote add upstream https://github.com/OCA/product-attribute
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/purchase-workflow.git
cd  purchase-workflow
git remote add upstream  https://github.com/OCA/purchase-workflow
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/reporting-engine
cd  reporting-engine
git remote add upstream https://github.com/OCA/reporting-engine
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/report-print-send.git
cd  report-print-send
git remote add upstream https://github.com/OCA/report-print-send
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/sale-workflow
cd  sale-workflow
git remote add upstream https://github.com/OCA/sale-workflow
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/server-tools.git
cd  server-tools
git remote add upstream https://github.com/OCA/server-tools
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/stock-logistics-tracking.git
cd  stock-logistics-tracking
git remote add upstream https://github.com/OCA/stock-logistics-tracking
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/stock-logistics-warehouse
cd stock-logistics-warehouse
git remote add upstream https://github.com/OCA/stock-logistics-warehouse
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/stock-logistics-workflow
cd stock-logistics-workflow
git remote add upstream https://github.com/OCA/stock-logistics-workflow
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/web.git
cd web
git remote add upstream  https://github.com/OCA/web
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/CybroAddons.git
cd CybroAddons
git remote add upstream https://github.com/CybroOdoo/CybroAddons
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/addons-vauxoo.git
cd addons-vauxoo
git remote add upstream https://github.com/Vauxoo/addons-vauxoo
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/SerpentCS_Contributions.git
cd SerpentCS_Contributions
git remote add upstream https://github.com/JayVora-SerpentCS/SerpentCS_Contributions
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/stock-logistics-reporting.git
cd stock-logistics-reporting
git remote add upstream https://github.com/OCA/stock-logistics-reporting
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/manufacture.git
cd manufacture
git remote add upstream https://github.com/OCA/manufacture
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/odoomrp-wip.git
cd odoomrp-wip
git remote add upstream https://github.com/odoomrp/odoomrp-wip
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/mail-addons.git
cd mail-addons
git remote add upstream https://github.com/it-projects-llc/mail-addons
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/stock-logistics-barcode.git
cd  stock-logistics-barcode
git remote add upstream https://github.com/OCA/stock-logistics-barcode
cd ..

git clone -b $OE_VERSION https://github.com/aaltinisik/techspawn-odoo-apps.git
cd  techspawn-odoo-apps
git remote add upstream https://github.com/techspawn/odoo-apps
cd ..


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

