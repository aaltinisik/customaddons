#!/bin/bash
# -*- encoding: utf-8 -*-

OE_HOME="/opt/$OE_USER/v$OE_VERSION"
OE_HOMEV="/opt/$OE_USER/v$OE_VER"
OE_HOME_EXT="$OE_HOMEV/$OE_USER-server"
OE_VERSION="12.0"
CLONE_REPOS=1
CREATE_ADDONS_LINKS=1
INSTALL_REQUIREMENTS=0
SRC_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
REPO_LIST_FILE=$SRC_PATH"/repo_list.txt"
ADDONS_LIST_FILE=$SRC_PATH"/addon_list.txt"
REQUIREMENTS_FILE=$SRC_PATH"/requirements.txt"

INSTALL_DIR=$OE_HOME
#USER=$(id -u)
OE_USER=$USER

clone_repos()
{ 

	if [ -z $REPO_LIST_FILE ] 
	then
		echo "Git repo list is not provided"
		exit
	elif [ ! -r $REPO_LIST_FILE ]
	then 
		echo "Git repo list file is not readable"
		exit
	else
	
		echo "Cloning custom repositories from file "$REPO_LIST_FILE
		
		if [ ! -d  $INSTALL_DIR"/repos" ]; then
			mkdir $INSTALL_DIR"/repos"
		fi
		
		if [ ! -d  $INSTALL_DIR"/addons" ]; then
			mkdir $INSTALL_DIR"/addons"
		fi

		
		cd $INSTALL_DIR"/repos"
		while read -r name upstream upstream_name ; 
		do
			git clone -b $OE_VERSION "https://github.com/aaltinisik/"$name $name
			cd "$name"
			if [ -z $upstream_name ]
			then
				git remote add upstream $upstream"/"$name
			else
				git remote add upstream $upstream"/"$upstream_name
			fi
			cd ..
			
		done < "$REPO_LIST_FILE"

	fi
	
	
}

create_sym_links()
{
	if [ -z $ADDONS_LIST_FILE ] 
	then
		echo "Addons list is not provided"
		exit 1
	elif [ ! -r $ADDONS_LIST_FILE ]
	then 
		echo "Addons list file is not readable"
		exit 1
	else
	
		cd $INSTALL_DIR
		
		if [ ! -d  "repos" ]; then
			echo "Repos folders does not exist"
			exit 1
		fi
		
		echo "Creating addons links from file "$ADDONS_LIST_FILE
		
		if [ ! -d  "addons" ]; then
			mkdir "addons"
		fi
		
		cd "addons"
		
		while read -r repo addon ; 
		do
			ln -s "../repos/$repo/$addon" "$addon"
			
		done < "$ADDONS_LIST_FILE"

	fi
}

usage()
{ 
	echo "install-customaddons.sh [option]"
	echo "    -C Do not create addon links"
	exit 1
}


while getopts 'Cd:Lru:v:' opt
do
  case $opt in
  	C) CLONE_REPOS=0 ;;
    d) 
    	if [[ $OPTARG == -* ]];
    	then 
    		echo "Invalid directory parameter"
    		exit 1
    	fi
    	if [ ! -d $OPTARG ];
    	then
    		echo "Creating installation directory $OPTARG"
    		mkdir $OPTARG
    	fi
    	INSTALL_DIR="$( cd $OPTARG ; pwd -P )"
    ;;
    u) OE_USER=$OPTARG ;;
    L) CREATE_ADDONS_LINKS=0 ;;
    r) INSTALL_REQUIREMENTS=1 ;;
    v) OE_VERSION=$OPTARG ;;
    ?) usage;;
	    
  esac
done




echo -e "\n---- : ----"
echo "Installing into "$INSTALL_DIR

if [ $INSTALL_REQUIREMENTS -ne 0 ];
then
	pip3 install -r $REQUIREMENTS_FILE
fi

if [ $CLONE_REPOS -ne 0 ];
then
	clone_repos
fi

if [ $CREATE_ADDONS_LINKS -ne 0 ];
then
	create_sym_links
fi

echo $USER
echo $OE_USER

if [ $USER != $OE_USER ];
then
	echo "Changing owner to "$OE_USER
	chown -R $OE_USER:$OE_USER $INSTALL_DIR
fi

exit 0


