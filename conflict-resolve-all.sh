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

cd $OCA_HOME

for D in *; do
   if [ -d "${D}" ];then
      echo "${D}"
      cd ${D}   # your processing here
      pwd
      git checkout $OE_VERSION
      if [ -n "$(git status --porcelain)" ]; then
          git status
          echo "there are changes in $D";
      read -p "Would you like to merge $D repo to Ours or Theirs or Pass (o/t/p)?" otp
  
      case $otp in
      [oO]*)
	  set -x 
          git checkout --ours .
          git add .
          git status
          git commit
	  git push
          cd ..
	  set +x
          ;;
      [tT]*)
          set -x 
          git checkout --theirs .
          git add .
	  git status
	  git commit
	  git push
          cd ..
          set +x
          ;;
       [pP]*)
       cd ..;;
       *)
       cd ..;;
    esac
  
        else
          echo "no changes in $D"
          cd ..;
      fi
  fi

done

