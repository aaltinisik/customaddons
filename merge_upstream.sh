#!/bin/bash
# -*- encoding: utf-8 -*-

##fixed parameters
#openerp

OE_USER="odoo"
OE_HOME="/opt/odoo"
OCA_HOME="/opt/odoo/v12/repos"
OE_HOME_EXT="/opt/odoo/odoo12"
# Replace for openerp-gevent for enabling gevent mode for chat
OE_SERVERTYPE="openerp-server"
OE_VERSION="12.0"
#set the superadmin password
OE_CONFIG="odoo-server"
git config --global credential.helper cache


echo -e "\n---- Install community Modules: ----"

cd $OCA_HOME

while true; do
    read -p "Would you like to git merge all repos from upstream repos (y/n)?" yn
    case $yn in
        [Yy]* ) cd $OCA_HOME

        for D in *; do
            if [ -d "${D}" ]; then
                echo "${D}"
                cd ${D}   # your processing here
                pwd
                git pull
                git remote -v
		git fetch upstream
		echo "Merging ...\n"
		git merge upstream/$OE_VERSION
		git commit -m "merge upstream $OE_VERSION"
		git push origin $OE_VERSION
                cd ..
		read -p "Press enter to continue"
            fi
        done

        break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done



