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



echo -e "\n---- Install community Modules: ----"

cd $OCA_HOME

while true; do
    read -p "Would you like to add new files commit and push to all repos of community modules (y/n)?" yn
    case $yn in
        [Yy]* ) cd $OCA_HOME

        for D in *; do
            if [ -d "${D}" ]; then
                echo "${D}"
                cd ${D}   # your processing here
                pwd
            		git add . -A
                git commit -m "$1"
                cd ..
            fi
        done

        break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done



