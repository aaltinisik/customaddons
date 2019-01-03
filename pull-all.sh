#!/bin/bash
# -*- encoding: utf-8 -*-

##fixed parameters
#openerp

OE_USER="odoo"
OE_HOME="/opt/odoo"
OCA_HOME="/opt/odoo/12/repos"
OE_HOME_EXT="/opt/odoo/odoo12"
# Replace for openerp-gevent for enabling gevent mode for chat
OE_SERVERTYPE="openerp-server"
OE_VERSION="12.0"
#set the superadmin password
OE_CONFIG="odoo-server"



echo -e "\n---- Install community Modules: ----"

cd $OCA_HOME

while true; do
    read -p "Would you like to git pull repos of community modules (y/n)?" yn
    case $yn in
        [Yy]* ) cd $OCA_HOME

        for D in *; do
            if [ -d "${D}" ]; then
                echo "${D}"
                cd ${D}   # your processing here
                pwd
                git pull
                cd ..
            fi
        done

        break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done



