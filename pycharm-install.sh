#!/bin/bash
# -*- encoding: utf-8 -*-

echo -e "\n---- add webupd8 java installer ppa ----"

# info on http://www.webupd8.org/2012/01/install-oracle-java-jdk-7-in-ubuntu-via.html
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java7-installer
echo -e "\n---- Check Java Version ----"
java -version
echo -e "\n---- add pycharms ppa ----"
sudo add-apt-repository ppa:mystic-mirage/pycharm
sudo apt-get update
sudo apt-get install pycharm-community



