#!/bin/bash
# -*- encoding: utf-8 -*-

##fixed parameters
#openerp

OE_USER="odoo"
OE_HOME="/opt/$OE_USER"
OCA_HOME="/opt/odoo/OCA"
OE_HOME_EXT="/opt/$OE_USER/$OE_USER-server"
# Replace for openerp-gevent for enabling gevent mode for chat
OE_SERVERTYPE="openerp-server"
OE_VERSION="8.0"
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

while true; do
    read -p "Would you like to git pull odoo repository (y/n)?" yn
    case $yn in
        [Yy]* )  cd $OE_HOME_EXT
        pwd
        git pull
        cd $OE_HOME/customaddons
        pwd
        git pull
        break;;
        [Nn]* ) break;;
        * )  echo "Please answer yes or no.";;
    esac
done

while true; do
    read -p "Would you like to update odoo database all  modules  (y/n)?" yn
    case $yn in
        [Yy]* ) cd $OE_HOME_EXT
        
        sudo /etc/init.d/odoo-server stop
        /opt/odoo/odoo-server/odooupdate.sh
        sudo /etc/init.d/odoo-server start
    
        break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

