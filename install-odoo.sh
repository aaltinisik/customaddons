#!/bin/bash
# -*- encoding: utf-8 -*-
################################################################################
#
#  Custom Changes made by Ahmet Altinisik
#
# Copyright (c) 2015 Luke Branch ( https://github.com/odoocommunitywidgets ) 
#               All Rights Reserved.
#               General Contact <odoocommunitywidgets@gmail.com>
#
# WARNING: This script as such is intended to be used by professional
# programmers/sysadmins who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company
#
# This script is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#upgrade1
# This script is distributed in the hope that it will be useful,
# but comes WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
################################################################################
# DESCRIPTION: This script is designed to install all the dependencies for the aeroo-reports modules from Alistek.
# It also gives you the option of installing Odoo while you're running the script. If you don't want this just choose no when given the option.


# use below if machine is VM
# sudo apt-get install open-vm-tools linux-virtual -y

echo -e "---- Decide system passwords ----"
read -e -s -p "Enter odoo system users password: " OE_USERPASS
echo -e "\n"
read -e -s -p "Enter the Database password: " DBPASS
echo -e "\n"
read -e -s -p "Enter the Odoo Administrator Password: " OE_SUPERADMIN
echo -e "\n"

echo 'Acquire::ForceIPv4 "true";' | tee /etc/apt/apt.conf.d/99force-ipv4
touch /etc/sysctl.d/disableipv6.conf
echo "net.ipv6.conf.all.disable_ipv6=1" >> /etc/sysctl.d/disableipv6.conf


sudo apt update
sudo apt upgrade -y
sudo apt install aptitude -y
sudo aptitude update && sudo aptitude full-upgrade -y
sudo apt build-dep build-essential -y

# Install Git:
echo -e "\n---- Install Git ----"
sudo apt install git -y

# Install pip
sudo apt install python-pip python3-pip -y

# sudo curl -O https://bootstrap.pypa.io/get-pip.py
# sudo python get-pip.py 



# Install AerooLib:
echo -e "\n---- Install AerooLib ----"
sudo apt install python-genshi python-cairo python-lxml libreoffice-script-provider-python libreoffice-base python-cups -y
sudo apt install python-setuptools python3-pip -yf
sudo mkdir /opt/aeroo
cd /opt/aeroo
sudo git clone https://github.com/aaltinisik/aeroolib.git
cd /opt/aeroo/aeroolib
sudo python setup.py install

#Create Init Script for OpenOffice (Headless Mode):
echo -e "\n---- create init script for LibreOffice (Headless Mode) ----"
sudo rm /etc/init.d/office
sudo touch /etc/init.d/office
sudo su root -c "echo '### BEGIN INIT INFO' >> /etc/init.d/office"
sudo su root -c "echo '# Provides:          office' >> /etc/init.d/office"
sudo su root -c "echo '# Required-Start:    $remote_fs $syslog' >> /etc/init.d/office"
sudo su root -c "echo '# Required-Stop:     $remote_fs $syslog' >> /etc/init.d/office"
sudo su root -c "echo '# Default-Start:     2 3 4 5' >> /etc/init.d/office"
sudo su root -c "echo '# Default-Stop:      0 1 6' >> /etc/init.d/office"
sudo su root -c "echo '# Short-Description: Start daemon at boot time' >> /etc/init.d/office"
sudo su root -c "echo '# Description:       Enable service provided by daemon.' >> /etc/init.d/office"
sudo su root -c "echo '### END INIT INFO' >> /etc/init.d/office"
sudo su root -c "echo '#! /bin/sh' >> /etc/init.d/office"
sudo su root -c "echo '/usr/bin/soffice --nologo --nofirststartwizard --headless --norestore --invisible \"--accept=socket,host=localhost,port=8100,tcpNoDelay=1;urp;\" &' >> /etc/init.d/office"

# Setup Permissions and test LibreOffice Headless mode connection

sudo chmod +x /etc/init.d/office
sudo update-rc.d office defaults

# Install AerooDOCS
echo -e "\n---- Install AerooDOCS (see: https://github.com/aeroo/aeroo_docs/wiki/Installation-example-for-Ubuntu-14.04-LTS for original post): ----"
# pip install --upgrade pip

sudo pip3 install jsonrpc2 daemonize

echo -e "\n---- create conf file for AerooDOCS ----"
sudo rm /etc/aeroo-docs.conf
sudo touch /etc/aeroo-docs.conf
sudo su root -c "echo '[start]' >> /etc/aeroo-docs.conf"
sudo su root -c "echo 'interface = localhost' >> /etc/aeroo-docs.conf"
sudo su root -c "echo 'port = 8989' >> /etc/aeroo-docs.conf"
sudo su root -c "echo 'oo-server = localhost' >> /etc/aeroo-docs.conf"
sudo su root -c "echo 'oo-port = 8100' >> /etc/aeroo-docs.conf"
sudo su root -c "echo 'spool-directory = /tmp/aeroo-docs' >> /etc/aeroo-docs.conf"
sudo su root -c "echo 'spool-expire = 1800' >> /etc/aeroo-docs.conf"
sudo su root -c "echo 'log-file = /var/log/aeroo-docs/aeroo_docs.log' >> /etc/aeroo-docs.conf"
sudo su root -c "echo 'pid-file = /tmp/aeroo-docs.pid' >> /etc/aeroo-docs.conf"
sudo su root -c "echo '[simple-auth]' >> /etc/aeroo-docs.conf"
sudo su root -c "echo 'username = anonymous' >> /etc/aeroo-docs.conf"
sudo su root -c "echo 'password = anonymous' >> /etc/aeroo-docs.conf"

cd /opt/aeroo
sudo git clone https://github.com/aaltinisik/aeroo_docs.git
sudo touch /etc/init.d/office
sudo python3 /opt/aeroo/aeroo_docs/aeroo-docs start -c /etc/aeroo-docs.conf

sudo cp /opt/aeroo/aeroo_docs/aeroo-docs.service /etc/systemd/system/aeroo-docs.service
sudo systemctl enable aeroo-docs.service
sudo systemctl daemon-reload
sudo systemctl start aeroo-docs.service


# If you encounter and error "Unable to lock on the pidfile while trying #16 just restart the service (sudo service aeroo-docs restart).
################################################################################
# Script for Installation: ODOO Saas4/Trunk server on Ubuntu 16.04 LTS
# Author: André Schenkels, ICTSTUDIO 2014
# Forked & Modified by: Luke Branch
# LibreOffice-Python 2.7 Compatibility Script Author: Holger Brunn (https://gist.github.com/hbrunn/6f4a007a6ff7f75c0f8b)
#-------------------------------------------------------------------------------
#  
# This script will install ODOO Server on
# clean Ubuntu 16.04 Server
#-------------------------------------------------------------------------------
# USAGE:
#
# odoo-install
#
# EXAMPLE:
# ./odoo-install 
#
################################################################################
 
##fixed parameters
#openerp
OE_USER="odoo"
OE_HOME="/opt/$OE_USER"
OE_HOME_EXT="/opt/$OE_USER/$OE_USER-server"
# Replace for openerp-gevent for enabling gevent mode for chat
OE_SERVERTYPE="openerp-server"
OE_VERSION="8.0"
#set the superadmin password
OE_CONFIG="odoo-server"

#--------------------------------------------------
# Set Locale en_US.UTF-8
#--------------------------------------------------
echo -e "\n---- Set en_US.UTF-8 Locale ----"
sudo cp /etc/default/locale /etc/default/locale.BACKUP
sudo rm -rf /etc/default/locale
echo -e "* Change server config file"
sudo su root -c "echo 'LC_ALL="en_US.UTF-8"' >> /etc/default/locale"
sudo su root -c "echo 'LANG="en_US.UTF-8"' >> /etc/default/locale"
sudo su root -c "echo 'LANGUAGE="en_US:en"' >> /etc/default/locale"

#-----------------------
# Odoo user 
echo -e "\n---- Enter odoo system users password ----"
sudo adduser odoo --home=/opt/odoo

read -n 1 -s -p "Press any key to continue"
#--------------------------------------------------
# Install PostgreSQL Server

sudo su root -c "echo 'deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main' >>  /etc/apt/sources.list"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
  sudo apt-key add -
sudo apt-get update

#--------------------------------------------------
echo -e "\n---- Install PostgreSQL Server ----"
sudo apt install postgresql postgresql-contrib -y  

echo -e "\n---- PostgreSQL $PG_VERSION Settings  ----"
sudo sed -i s/"#listen_addresses = 'localhost'"/"listen_addresses = '*'"/g /etc/postgresql/9.6/main/postgresql.conf

echo -e "\n---- Enter password for ODOO PostgreSQL User  ----"
sudo su - postgres -c "createuser --createdb --username postgres $OE_USER" 
# sudo su - postgres -c 'ALTER USER $OE_USER WITH SUPERUSER;'
echo -e "\n---- Creating postgres unaccent search extension  ----"
sudo su - postgres -c 'psql template1 -c "CREATE EXTENSION \"unaccent\"";'

sudo -u postgres psql -U postgres -d postgres -c "alter user $OE_USER with password '$DBPASS';"

# sudo adduser --shell=/bin/bash --home=/opt/$OE_USER --gecos "Odoo" $OE_USER

# echo $OE_USER:$OE_USERPASS | chpasswd

echo -e "\n---- Create Log directory ----"
sudo mkdir /var/log/$OE_USER
sudo chown $OE_USER:$OE_USER /var/log/$OE_USER


echo -e "\n---- Install Wkhtmltopdf 0.12.1 ----"
sudo wget -P Downloads https://github.com/aaltinisik/customaddons/blob/8.0/wkhtmltox-0.12.2.1_linux-trusty-amd64.deb?raw=true

sudo apt-get install -f -y
sudo apt-get install wkhtmltox -y
sudo dpkg -i Downloads/wkhtmltox-0.12.2.1_linux-trusty-amd64.deb

sudo cp /usr/local/bin/wkhtmltopdf /usr/bin
sudo cp /usr/local/bin/wkhtmltoimage /usr/bin


#--------------------------------------------------
# Install ODOO
#--------------------------------------------------
echo -e "\n==== Installing ODOO Server ===="
sudo su $OE_USER -c "git clone  --depth 1 --branch 8.0 https://github.com/aaltinisik/OCBAltinkaya.git $OE_HOME_EXT/"

echo -e "\n---- Create custom module directory ----"
sudo su $OE_USER -c "mkdir $OE_HOME/custom"
sudo su $OE_USER -c "mkdir $OE_HOME/custom/addons"

echo -e "\n---- Setting permissions on home folder ----"
sudo chown -R $OE_USER:$OE_USER $OE_HOME/*

echo -e "* Create server config file"

sudo rm /etc/$OE_CONFIG.conf
sudo touch /etc/$OE_CONFIG.conf
sudo chown $OE_USER:$OE_USER /etc/$OE_CONFIG.conf
sudo chmod 640 /etc/$OE_CONFIG.conf

echo -e "* Change server config file"

sudo su root -c "echo '[options]' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'db_host = localhost' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'db_user = $OE_USER' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'db_port = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'db_password = $DBPASS' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'admin_passwd = $OE_SUPERADMIN' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'addons_path = $OE_HOME_EXT/addons,$OE_HOME/custom/addons,$OE_HOME/customaddons' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## Server startup config - Common options' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Admin password for creating, restoring and backing up databases admin_passwd = admin' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify additional addons paths (separated by commas)' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## XML-RPC / HTTP - XML-RPC Configuration' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'unaccent = True' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'xmlrpc = True' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Specify the TCP IP address for the XML-RPC protocol. The empty string binds to all interfaces.' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'xmlrpc_interface  = ' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the TCP port for the XML-RPC protocol' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'xmlrpc_port = 8069' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Enable correct behavior when behind a reverse proxy' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'proxy_mode = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## XML-RPC / HTTPS - XML-RPC Secure Configuration' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# disable the XML-RPC Secure protocol' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'xmlrpcs = True' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Specify the TCP IP address for the XML-RPC Secure protocol. The empty string binds to all interfaces.' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'xmlrpcs_interface = ' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the TCP port for the XML-RPC Secure protocol' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'xmlrpcs_port = 8071' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the certificate file for the SSL connection' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'secure_cert_file = server.cert' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the private key file for the SSL connection' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'secure_pkey_file = server.pkey' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## NET-RPC - NET-RPC Configuration' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# enable the NETRPC protocol' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'netrpc = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the TCP IP address for the NETRPC protocol' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'netrpc_interface = 127.0.0.1' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the TCP port for the NETRPC protocol' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'netrpc_port = 8070' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## WEB - Web interface Configuration' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Filter listed database REGEXP' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'dbfilter = .*' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## Static HTTP - Static HTTP service' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# enable static HTTP service for serving plain HTML files' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'static_http_enable = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the directory containing your static HTML files (e.g '/var/www/')' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'static_http_document_root = None' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the URL root prefix where you want web browsers to access your static HTML files (e.g '/')' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'static_http_url_prefix = None' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## Testing Group - Testing Configuration' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Launch a YML test file.' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'test_file = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# If set, will save sample of all reports in this directory.' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'test_report_directory = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Enable YAML and unit tests.' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## Server startup config - Common options' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'test_disable = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Commit database changes performed by YAML or XML tests.' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'test_commit = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '## Logging Group - Logging Configuration' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# file where the server log will be stored (default = None)' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'logfile = /var/log/$OE_USER/$OE_CONFIG$1.log' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# do not rotate the logfile' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'logrotate = True' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# Send the log to the syslog server' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'syslog = False' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# setup a handler at LEVEL for a given PREFIX. An empty PREFIX indicates the root logger. This option can be repeated. Example: "openerp.orm:DEBUG" or "werkzeug:CRITICAL" (default: ":INFO")' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'log_handler = ["[':INFO']"]' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '# specify the level of the logging. Accepted values: info, debug_rpc, warn, test, critical, debug_sql, error, debug, debug_rpc_answer, notset' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo '#log_level = debug' >> /etc/$OE_CONFIG.conf"
sudo su root -c "echo 'log_level = info' >> /etc/$OE_CONFIG.conf"


echo -e "* Create startup file"
sudo su root -c "rm $OE_HOME_EXT/start.sh"
sudo su root -c "echo '#!/bin/sh' >> $OE_HOME_EXT/start.sh"
sudo su root -c "echo 'sudo -u $OE_USER $OE_HOME_EXT/$OE_SERVERTYPE --config=/etc/$OE_CONFIG.conf' >> $OE_HOME_EXT/start.sh"
sudo chmod 755 $OE_HOME_EXT/start.sh

#--------------------------------------------------
# Adding ODOO as a deamon (initscript)
#--------------------------------------------------

echo -e "* Create init file"
echo '#!/bin/sh' >> ~/$OE_CONFIG
echo '### BEGIN INIT INFO' >> ~/$OE_CONFIG
echo '# Provides: $OE_CONFIG' >> ~/$OE_CONFIG
echo '# Required-Start: $remote_fs $syslog' >> ~/$OE_CONFIG
echo '# Required-Stop: $remote_fs $syslog' >> ~/$OE_CONFIG
echo '# Should-Start: $network' >> ~/$OE_CONFIG
echo '# Should-Stop: $network' >> ~/$OE_CONFIG
echo '# Default-Start: 2 3 4 5' >> ~/$OE_CONFIG
echo '# Default-Stop: 0 1 6' >> ~/$OE_CONFIG
echo '# Short-Description: Enterprise Business Applications' >> ~/$OE_CONFIG
echo '# Description: ODOO Business Applications' >> ~/$OE_CONFIG
echo '### END INIT INFO' >> ~/$OE_CONFIG
echo 'PATH=/bin:/sbin:/usr/bin' >> ~/$OE_CONFIG
echo "DAEMON=$OE_HOME_EXT/$OE_SERVERTYPE" >> ~/$OE_CONFIG
echo "NAME=$OE_CONFIG" >> ~/$OE_CONFIG
echo "DESC=$OE_CONFIG" >> ~/$OE_CONFIG
echo '' >> ~/$OE_CONFIG
echo '# Specify the user name (Default: odoo).' >> ~/$OE_CONFIG
echo "USER=$OE_USER" >> ~/$OE_CONFIG
echo '' >> ~/$OE_CONFIG
echo '# Specify an alternate config file (Default: /etc/openerp-server.conf).' >> ~/$OE_CONFIG
echo "CONFIGFILE=\"/etc/$OE_CONFIG.conf\"" >> ~/$OE_CONFIG
echo '' >> ~/$OE_CONFIG
echo '# pidfile' >> ~/$OE_CONFIG
echo 'PIDFILE=/var/run/$NAME.pid' >> ~/$OE_CONFIG
echo '' >> ~/$OE_CONFIG
echo '# Additional options that are passed to the Daemon.' >> ~/$OE_CONFIG
echo 'DAEMON_OPTS="-c $CONFIGFILE"' >> ~/$OE_CONFIG
echo '[ -x $DAEMON ] || exit 0' >> ~/$OE_CONFIG
echo '[ -f $CONFIGFILE ] || exit 0' >> ~/$OE_CONFIG
echo 'checkpid() {' >> ~/$OE_CONFIG
echo '[ -f $PIDFILE ] || return 1' >> ~/$OE_CONFIG
echo 'pid=`cat $PIDFILE`' >> ~/$OE_CONFIG
echo '[ -d /proc/$pid ] && return 0' >> ~/$OE_CONFIG
echo 'return 1' >> ~/$OE_CONFIG
echo '}' >> ~/$OE_CONFIG
echo '' >> ~/$OE_CONFIG
echo 'case "${1}" in' >> ~/$OE_CONFIG
echo 'start)' >> ~/$OE_CONFIG
echo 'echo -n "Starting ${DESC}: "' >> ~/$OE_CONFIG
echo 'start-stop-daemon --start --quiet --pidfile ${PIDFILE} \' >> ~/$OE_CONFIG
echo '--chuid ${USER} --background --make-pidfile \' >> ~/$OE_CONFIG
echo '--exec ${DAEMON} -- ${DAEMON_OPTS}' >> ~/$OE_CONFIG
echo 'echo "${NAME}."' >> ~/$OE_CONFIG
echo ';;' >> ~/$OE_CONFIG
echo 'stop)' >> ~/$OE_CONFIG
echo 'echo -n "Stopping ${DESC}: "' >> ~/$OE_CONFIG
echo 'start-stop-daemon --stop --quiet --pidfile ${PIDFILE} \' >> ~/$OE_CONFIG
echo '--oknodo' >> ~/$OE_CONFIG
echo 'echo "${NAME}."' >> ~/$OE_CONFIG
echo ';;' >> ~/$OE_CONFIG
echo '' >> ~/$OE_CONFIG
echo 'restart|force-reload)' >> ~/$OE_CONFIG
echo 'echo -n "Restarting ${DESC}: "' >> ~/$OE_CONFIG
echo 'start-stop-daemon --stop --quiet --pidfile ${PIDFILE} \' >> ~/$OE_CONFIG
echo '--oknodo' >> ~/$OE_CONFIG
echo 'sleep 1' >> ~/$OE_CONFIG
echo 'start-stop-daemon --start --quiet --pidfile ${PIDFILE} \' >> ~/$OE_CONFIG
echo '--chuid ${USER} --background --make-pidfile \' >> ~/$OE_CONFIG
echo '--exec ${DAEMON} -- ${DAEMON_OPTS}' >> ~/$OE_CONFIG
echo 'echo "${NAME}."' >> ~/$OE_CONFIG
echo ';;' >> ~/$OE_CONFIG
echo '*)' >> ~/$OE_CONFIG
echo 'N=/etc/init.d/${NAME}' >> ~/$OE_CONFIG
echo 'echo "Usage: ${NAME} {start|stop|restart|force-reload}" >&2' >> ~/$OE_CONFIG
echo 'exit 1' >> ~/$OE_CONFIG
echo ';;' >> ~/$OE_CONFIG
echo '' >> ~/$OE_CONFIG
echo 'esac' >> ~/$OE_CONFIG
echo 'exit 0' >> ~/$OE_CONFIG

echo -e "* Security Init File"
sudo mv ~/$OE_CONFIG /etc/init.d/$OE_CONFIG
sudo chmod 755 /etc/init.d/$OE_CONFIG
sudo chown root: /etc/init.d/$OE_CONFIG

echo -e "* Create service   sudo service $OE_SERVERTYPE start"
sudo update-rc.d $OE_SERVERTYPE defaults

echo -e "* Open ports in UFW for openerp-gevent"
sudo ufw allow 8072
echo -e "* Open ports in UFW for openerp-server"
sudo ufw allow 8069

echo -e "* Start ODOO on Startup"
sudo update-rc.d $OE_CONFIG defaults

read -n 1 -s -p "Press any key to continue"
#--------------------------------------------------
# Install Dependencies
#--------------------------------------------------
#--------------------------------------------------
# Install SSH
#--------------------------------------------------
echo -e "\n---- Install SSH Server ----"
sudo apt install ssh -y
echo -e "\n---- Install tool packages ----"
sudo apt install wget subversion git bzr bzrtools python-pip -y

echo -e "\n---- Install and Upgrade pip and virtualenv ----"
sudo apt install python-dev build-essential -y
sudo pip install --upgrade pip
sudo pip install --upgrade virtualenv

echo -e "\n---- Install pyserial and qrcode for compatibility with hw_ modules for peripheral support in Odoo ---"

sudo pip install jcconv

echo -e "\n---- Install pyusb 1.0+ not stable for compatibility with hw_escpos for receipt printer and cash drawer support in Odoo ---"
sudo pip install --pre pyusb

echo -e "\n---- Install python packages ----"
sudo apt install -y -f poppler-utils postgresql-client python-cairo python-cups python-dateutil python-decorator python-docutils python-egenix-mxdatetime \
python-feedparser python-gdata python-genshi python-geoip python-gevent python-imaging python-jinja2 python-ldap python-libxslt1 \
python-lxml python-mako python-markupsafe python-matplotlib python-mock python-openid python-openssl python-passlib \
python-pdftools python-psutil python-psycopg2 python-pybabel python-pychart python-pydot python-pyparsing python-qrcode python-serial \
python-pypdf python-reportlab python-reportlab-accel python-requests python-setuptools python-simplejson python-tz python-unicodecsv \
python-unittest2 python-vatnumber python-vatnumber python-vobject python-webdav python-werkzeug python-xlwt python-yaml python-zsi \
vim wkhtmltopdf curl ghostscript libpq-dev libreoffice libreoffice-script-provider-python xfonts-base xfonts-75dpi


# Install NodeJS and Less compiler needed by Odoo 8 Website - added from https://gist.github.com/rm-jamotion/d61bc6525f5b76245b50
# wget -qO- https://deb.nodesource.com/setup | sudo -E bash -
wget -qO- https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt install nodejs -y
sudo npm install -g less -y
sudo npm install node-odoo

echo -e "\n---- Install python libraries ----"
sudo apt-get install graphviz mc bzr lptools make -y

sudo apt-get install -y python-unidecode python-pygraphviz python-psycopg2

echo -e "\n---- Install Other Dependencies ----"
sudo pip install psycogreen

echo -e "\n---- Install asterisk connector dependencies ----"
sudo pip install phonenumbers
sudo pip install py-Asterisk



sudo apt-get install cups lpr phppgadmin -y
sudo apt-get install foomatic-db openprinting-ppds foomatic-db-gutenprint python-notify lm-sensors snmp-mibs-downloader psutils hannah-foo2zjs tix hpijs-ppds python-pexpect-doc unpaper tcl-tclreadline xfonts-cyrillic -y
sudo apt-get autoremove -y
sudo apt-get -f install -y

#sudo cp /etc/apache2/conf.d/phppgadmin /etc/apache2/conf-enabled/phppgadmin.conf

# Install Aeroo Reports:
echo -e "\n---- Install Aeroo Reports Odoo Modules: ----"

        cd $OE_HOME
        sudo su $OE_USER -c "git clone -b 8.0 https://github.com/aaltinisik/customaddons.git"
        sudo su $OE_USER -c "mkdir OCA"
        sudo su $OE_USER -c "cd OCA"        
        sudo su $OE_USER -c "git clone -b 8.0 https://github.com/aaltinisik/aeroo_reports"
        sudo su $OE_USER -c "git clone -b 8.0 https://github.com/aaltinisik/connector-telephony.git"
        sudo su $OE_USER -c "ln -s -f $OE_HOME/OCA/connector-telephony/* $OE_HOME/custom/addons/"
        sudo su $OE_USER -c "ln -s -f $OE_HOME/OCA/aeroo_reports/* $OE_HOME/custom/addons/"
        
        sudo su $OE_USER -c "git clone -b 8.0 https://github.com/OCA/web.git"
        sudo su $OE_USER -c "git clone -b 8.0 https://github.com/yelizariev/addons-yelizariev.git"
        sudo su $OE_USER -c "git clone -b 8.0 https://github.com/OCA/server-tools.git"
        sudo su $OE_USER -c "git clone -b 8.0 https://github.com/OCA/knowledge.git"
        sudo su $OE_USER -c "git clone -b 8.0 https://github.com/OCA/purchase-workflow.git"
        sudo su $OE_USER -c "git clone -b 8.0 https://github.com/OCA/product-attribute.git"
        sudo su $OE_USER -c "git clone -b 8.0 https://github.com/OCA/sale-workflow.git"
        sudo su $OE_USER -c "git clone -b 8.0 https://github.com/OCA/account-invoicing.git"
        sudo su $OE_USER -c "git clone -b 8.0 https://github.com/OCA/stock-logistics-tracking.git"
        


OCA_HOME="$OE_HOME/OCA"

        cd $OE_HOME
        sudo su $OE_USER -c "git clone -b $OE_VERSION https://github.com/aaltinisik/customaddons.git $OE_HOME/customaddons"
        sudo su $OE_USER -c "mkdir $OCA_HOME"
        sudo su $OE_USER -c "cd $OCA_HOME"
        sudo su $OE_USER -c "git clone -b $OE_VERSION https://github.com/aaltinisik/aeroo_reports $OCA_HOME/aeroo_reports"
        sudo su $OE_USER -c "git clone -b $OE_VERSION https://github.com/aaltinisik/connector-telephony.git $OCA_HOME/connector-telephony"    
        sudo su $OE_USER -c "git clone -b $OE_VERSION https://github.com/OCA/web.git $OCA_HOME/web"
        sudo su $OE_USER -c "git clone -b $OE_VERSION https://github.com/yelizariev/addons-yelizariev.git $OCA_HOME/addons-yelizariev"
        sudo su $OE_USER -c "git clone -b $OE_VERSION https://github.com/OCA/server-tools.git $OCA_HOME/server-tools"
        sudo su $OE_USER -c "git clone -b $OE_VERSION https://github.com/OCA/knowledge.git $OCA_HOME/knowledge"
        sudo su $OE_USER -c "git clone -b $OE_VERSION https://github.com/OCA/purchase-workflow.git $OCA_HOME/purchase-workflow"
        sudo su $OE_USER -c "git clone -b $OE_VERSION https://github.com/OCA/product-attribute.git $OCA_HOME/product-attribute"
        sudo su $OE_USER -c "git clone -b $OE_VERSION https://github.com/OCA/sale-workflow.git $OCA_HOME/sale-workflow"
        sudo su $OE_USER -c "git clone -b $OE_VERSION https://github.com/OCA/account-invoicing.git $OCA_HOME/account-invoicing"
        sudo su $OE_USER -c "git clone -b $OE_VERSION https://github.com/OCA/stock-logistics-tracking.git $OCA_HOME/stock-logistics-tracking"
        sudo su $OE_USER -c "git clone -b $OE_VERSION https://github.com/OCA/partner-contact.git $OCA_HOME/partner-contact"

cd $OE_HOME
sudo su $OE_USER -c "ln -s -f $OCA_HOME/connector-telephony/* $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/aeroo_reports/* $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/aeroo_reports/* $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/web/web_widget_many2many_tags_multi_selection $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/web/web_translate_dialog $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/web/web_sheet_full_width $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/web/web_searchbar_full_width $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/web/web_last_viewed_records $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/server-tools/auth_admin_passkey $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/server-tools/base_concurrency $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/server-tools/admin_technical_features $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/server-tools/cron_run_manually $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/web/web_environment_ribbon $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/server-tools/scheduler_error_mailer $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/server-tools/base_optional_quick_create $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/server-tools/base_report_auto_create_qweb $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/server-tools/disable_openerp_online $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/server-tools/fetchmail_notify_error_to_sender $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/server-tools/language_path_mixin $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/server-tools/module_prototyper $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/server-tools/mass_editing $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/server-tools/super_calendar $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/knowledge/attachment_preview $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/knowledge/attachments_to_filesystem $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/purchase-workflow/product_by_supplier $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/purchase-workflow/purchase_order_revision $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/partner-contact/partner_external_maps $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/product-attribute/product_dimension $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/product-attribute/product_weight $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/sale-workflow/partner_prepayment $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/sale-workflow/sale_automatic_workflow $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/sale-workflow/sale_cancel_reason $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/sale-workflow/sale_order_back2draft $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/sale-workflow/partner_prepayment $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/sale-workflow/sale_automatic_workflow $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/sale-workflow/sale_cancel_reason $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/sale-workflow/sale_order_back2draft $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/sale-workflow/sale_order_price_recalculation $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/sale-workflow/sale_order_revision $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/sale-workflow/sale_partner_incoterm $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/sale-workflow/sale_payment_method $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/sale-workflow/sale_validity $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/account-invoicing/account_invoice_partner $OE_HOME/custom/addons/"
sudo su $OE_USER -c "ln -s -f $OCA_HOME/stock-logistics-tracking/stock_barcode_reader $OE_HOME/custom/addons/"


echo "Done! The ODOO server can be started with /etc/init.d/$OE_CONFIG"
echo "Please reboot the server now so that Wkhtmltopdf is working with your install."
echo "Once you've rebooted you'll be able to access your Odoo instance by going to http://[your server's IP address]:8069"
echo "For example, if your server's IP address is 192.168.1.123 you'll be able to access it on http://192.168.1.123:8069"

echo -e "\n >>>>>>>>>> PLEASE RESTART YOUR SERVER TO FINALISE THE INSTALLATION (See below for the command you should use) <<<<<<<<<<"
echo -e "\n---- restart the server (sudo shutdown -r now) ----"
while true; do
    read -p "Would you like to restart your server now (y/n)?" yn
    case $yn in
        [Yy]* ) sudo shutdown -r now
        break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

