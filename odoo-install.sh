#!/bin/bash
################################################################################
# Addtions by Ahmet Altinisik dec 2019
# Script for installing Odoo on Ubuntu 14.04, 15.04, 16.04 and 18.04 (could be used for other version too)
# Author: Yenthe Van Ginneken
#-------------------------------------------------------------------------------
# This script will install Odoo on your Ubuntu 16.04 server. It can install multiple Odoo instances
# in one Ubuntu because of the different xmlrpc_ports
#-------------------------------------------------------------------------------
# Make a new file:
# sudo nano odoo-install.sh
# Place this content in it and then make the file executable:
# sudo chmod +x odoo-install.sh
# Execute the script to install Odoo:
# ./odoo-install
################################################################################
OE_VER="12"
OE_USER="odoo"
OE_HOME="/opt/$OE_USER"
Oe_HOMEV="/opt/$OE_USER/v$OE_VERSION"
OE_HOME_EXT="/opt/$OE_USER/v$OE_VERSION/${OE_USER}-server"
# The default port where this Odoo instance will run under (provided you use the command -c in the terminal)
# Set to true if you want to install it, false if you don't need it or have it already installed.
INSTALL_WKHTMLTOPDF="True"
# Set the default Odoo port (you still have to use -c /etc/odoo-server.conf for example to use this.)
OE_PORT="8069"
# Choose the Odoo version which you want to install. For example: 13.0, 12.0, 11.0 or saas-18. When using 'master' the master version will be installed.
# IMPORTANT! This script contains extra libraries that are specifically needed for Odoo 13.0
OE_VERSION=$OE_VER".0"
# Set this to True if you want to install the Odoo enterprise version!
IS_ENTERPRISE="False"
# set the superadmin password
OE_CONFIG="${OE_USER}-$OE_VER"

echo -e "---- Decide system passwords ----"
read -e -s -p "Enter odoo system users password: " OE_USERPASS
echo -e "\n"
read -e -s -p "Enter the Database password: " DBPASS
echo -e "\n"
read -e -s -p "Enter the Odoo Administrator Password: " OE_SUPERADMIN
echo -e "\n"


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
sudo adduser odoo --home=$OE_HOME

read -n 1 -s -p "Press any key to continue"
#--------------------------------------------------

#Disable ipv6 for apt


sudo echo 'Acquire::ForceIPv4 "true";' | tee /etc/apt/apt.conf.d/99force-ipv4



##
###  WKHTMLTOPDF download links
## === Ubuntu Trusty x64 & x32 === (for other distributions please replace these two links,
## in order to have correct version of wkhtmltopdf installed, for a danger note refer to 
## https://github.com/odoo/odoo/wiki/Wkhtmltopdf ):
WKHTMLTOX_X64=https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.trusty_amd64.deb
WKHTMLTOX_X32=https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.trusty_i386.deb

#--------------------------------------------------
# Update Server
#--------------------------------------------------
echo -e "\n---- Update Server ----"
# universe package is for Ubuntu 18.x
sudo add-apt-repository universe
# libpng12-0 dependency for wkhtmltopdf
sudo add-apt-repository "deb http://mirrors.kernel.org/ubuntu/ xenial main"
sudo apt-get update
sudo apt-get upgrade -y

#--------------------------------------------------
# Install PostgreSQL Server from postgresql repo
#--------------------------------------------------

echo -e "\n---- Install PostgreSQL Server ----"
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-11  postgresql-contrib -y

#--------------------------------------------------
# Install Dependencies
#--------------------------------------------------
echo -e "\n--- Installing Python 3 + pip3 --"
sudo apt-get install git python3 python3-pip build-essential wget python3-dev python3-venv python3-wheel libxslt-dev libzip-dev libldap2-dev libsasl2-dev python3-setuptools node-less libpng12-0 gdebi -y

echo -e "\n---- Install python packages/requirements ----"
sudo pip3 install -r https://github.com/odoo/odoo/raw/${OE_VERSION}/requirements.txt

echo -e "\n---- Installing nodeJS NPM and rtlcss for LTR support ----"
sudo apt-get install nodejs npm -y
sudo npm install -g rtlcss

#--------------------------------------------------
# Install Wkhtmltopdf if needed
#--------------------------------------------------
if [ $INSTALL_WKHTMLTOPDF = "True" ]; then
  echo -e "\n---- Install wkhtml and place shortcuts on correct place for ODOO 13 ----"
  #pick up correct one from x64 & x32 versions:
  if [ "`getconf LONG_BIT`" == "64" ];then
      _url=$WKHTMLTOX_X64
  else
      _url=$WKHTMLTOX_X32
  fi
  sudo wget $_url
  sudo gdebi --n `basename $_url`
  sudo ln -s /usr/local/bin/wkhtmltopdf /usr/bin
  sudo ln -s /usr/local/bin/wkhtmltoimage /usr/bin
else
  echo "Wkhtmltopdf isn't installed due to the choice of the user!"
fi

echo -e "\n---- Create Log directory ----"
sudo mkdir /var/log/$OE_USER
sudo chown $OE_USER:$OE_USER /var/log/$OE_USER

#--------------------------------------------------
# Install ODOO
#--------------------------------------------------

echo -e "\n---- Create custom module directory ----"
echo -e "\n create $OE_HOMEV,$OE_HOMEV/repos,$OE_HOMEV/addons"
sudo su $OE_USER -c "mkdir $OE_HOMEV"
sudo su $OE_USER -c "mkdir $OE_HOMEV/repos"
sudo su $OE_USER -c "mkdir $OE_HOMEV/addons"

echo -e "\n---- Setting permissions on home folder ----"
sudo chown -R $OE_USER:$OE_USER $OE_HOME/*


echo -e "\n==== Installing ODOO Server ===="

sudo git clone --depth 1 --branch $OE_VERSION https://github.com/aaltinisik/OCBAltinkaya.git $OE_HOME_EXT/
cd $OE_HOMEV

sudo git clone --depth 1 --branch $OE_VERSION https://www.github.com/aaltinisik/customaddons.git

$OE_HOMEV/customaddons/install-customaddons.sh


echo -e "* Create server config file"

sudo touch /etc/${OE_CONFIG}.conf
echo -e "* Creating server config file"
sudo su root -c "printf '[options] \n; This is the password that allows database operations:\n' >> /etc/${OE_CONFIG}.conf"
sudo su root -c "printf 'admin_passwd = ${OE_SUPERADMIN}\n' >> /etc/${OE_CONFIG}.conf"
sudo su root -c "printf 'xmlrpc_port = ${OE_PORT}\n' >> /etc/${OE_CONFIG}.conf"
sudo su root -c "printf 'logfile = /var/log/${OE_USER}/${OE_CONFIG}.log\n' >> /etc/${OE_CONFIG}.conf"
sudo su root -c "printf 'addons_path=${OE_HOME_EXT}/addons,${OE_HOMEV}/addons,$OE_HOME/customaddons\n' >> /etc/${OE_CONFIG}.conf"

sudo chown $OE_USER:$OE_USER /etc/${OE_CONFIG}.conf
sudo chmod 640 /etc/${OE_CONFIG}.conf

echo -e "* Create startup file"
sudo su root -c "echo '#!/bin/sh' >> $OE_HOME_EXT/start.sh"
sudo su root -c "echo 'sudo -u $OE_USER $OE_HOME_EXT/odoo-bin --config=/etc/${OE_CONFIG}.conf' >> $OE_HOME_EXT/start.sh"
sudo chmod 755 $OE_HOME_EXT/start.sh

#--------------------------------------------------
# Adding ODOO as a systemD daemon (initscript)
#--------------------------------------------------


echo -e "* SystemD Init File"

sudo cp /opt/odoo/odoo-server/debian/odoo.service /etc/systemd/system/odoo.service
sudo chmod 755 /etc/systemd/system/odoo.service
sudo chown root: /etc/systemd/system/odoo.service
sudo systemctl enable odoo.service


echo -e "* Open ports in UFW for odoo-server"
sudo ufw allow $OE_PORT

sudo systemctl start odoo.service


echo "Done! The ODOO server can be started with sudo systemctl start odoo.service"
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



