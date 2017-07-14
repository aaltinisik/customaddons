#!/bin/bash

echo -e "---- Database Anonymize ----"
read -e -p "Enter odoo database to anonymize: " DBNAME
#--------------------------------------------------

sudo /etc/init.d/odoo-server stop

/opt/odoo/odoo-server/odoo.py -d $DBNAME -i anonymization --without-demo=all --stop-after-init --config=/etc/odoo-server.conf --workers=0 --max-cron-threads=0

psql -f ./anonymize.sql -a -d $DBNAME

python ./anonymize.py +action a +file $DBNAME_anonymize.pickle +t 8.0 +db $DBNAME

psql -d $DBNAME -c "VACUUM FULL;"

sudo reboot
