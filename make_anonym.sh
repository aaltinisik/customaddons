#!/bin/bash

echo -e "---- Database Anonymize ----"
read -e -p "Enter odoo database to anonymize: " DBNAME
#--------------------------------------------------

if [ "$(id -u)" = "0" ]; then
   echo "This script must not be run as root" 1>&2
   exit 1
fi

while true; do
    read -p "Would you like to install anonymization module, odoo server will stop during process  (y/n)?" yn
    case $yn in
        [Yy]* ) 
        sudo service odoo stop
        echo -e "Installing Module"
        /opt/odoo/odoo-server/odoo.py -d $DBNAME -i anonymization  --without-demo=all --stop-after-init --config=/etc/odoo-server.conf --workers=0 --max-cron-threads=0
        sudo service odoo start
        break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

BEEP="/usr/share/sounds/ubuntu/stereo/phone-incoming-call.ogg"

sudo service odoo stop

/opt/odoo/odoo-server/odoo.py -d $DBNAME -i anonymization --without-demo=all --stop-after-init --config=/etc/odoo-server.conf --workers=0 --max-cron-threads=0

psql -f ./anonymize.sql -a -d $DBNAME

python ./anonymize.py +action a +file $DBNAME_anonymize.pickle +t 8.0 +db $DBNAME

psql -d $DBNAME -c "VACUUM FULL;"
paplay $BEEP

