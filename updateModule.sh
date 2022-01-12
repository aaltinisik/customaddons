#!/bin/bash

if [ "$(id -u)" = "0" ]; then
   echo "This script must not be run as root" 1>&2
   exit 1
fi

while true; do
    read -p "Would you like to update modules, odoo server will stop during process  (y/n)?" yn
    case $yn in
        [Yy]* ) 
	echo -e "stopping odoo server"
        sudo systemctl stop odoo
        echo -e "Updating Modules"
        cd /opt/odoo/V8/odoo-server
        /opt/odoo/V8/odoo-server/openerp-server -d $1 -u $2 --stop-after-init --config=/etc/odoo-8.conf --workers=0 --max-cron-threads=0
	sudo tail  /var/log/odoo/odoo-server.log
        echo *e "Starting odoo server"
	sudo systemctl start odoo
        break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

