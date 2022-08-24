#!/bin/sh
PKG_NAME="yt-notify"
INSTALL_FOLDER="/opt/"
LINK_FOLDER="/usr/bin/"
TOTAL_INSTALL=$INSTALL_FOLDER$PKG_NAME
LOGIN_NAME=$(logname)
PYTHON_EXE=$(which python3)
PYTHON_INSERT_1="#!${PYTHON_EXE}"
PYTHON_INSERT_2="os.chdir(\"${TOTAL_INSTALL}/\")"
TEMP_DIR=$(cat /dev/random | strings | grep -m 1 -oEi '[a-zA-Z0-9]{10}')

if [ ! ${EUID} -eq 0 ]; then
  echo "Please run as sudo"
  exit
fi

printf "This script installs '${PKG_NAME}'\n 
it places the files in ${INSTALL_FOLDER}  
and places a symbolic link in ${LINK_FOLDER}\n
Continue?(y/n): "

while read answer
do
  case $answer in
        yes|y)      break    ;;
        no|n)       exit   ;;
        *)              
                ;;
   esac
done

Test_Exit_Status () {
    if [ $? -eq 1 ]
    then
        rm -r /tmp/$TEMP_DIR
        printf "\nError installing! Problem with: $1\n"
        exit
    fi
}

shopt -s extglob
mkdir -v /tmp/$TEMP_DIR && \
cp -rv !(setup.sh) /tmp/$TEMP_DIR && \
cd /tmp/$TEMP_DIR
Test_Exit_Status "temporary directory /tmp/"
shopt -u extglob

sed -iv "1 i$PYTHON_INSERT_1" ./main.py && \
sed -iv "14 i$PYTHON_INSERT_2" ./main.py && \
mv -v ./main.py $PKG_NAME
Test_Exit_Status "sed changing source code"

mkdir -pv $TOTAL_INSTALL && \
cp -rv ./* $TOTAL_INSTALL && \
ln -sfv $TOTAL_INSTALL/$PKG_NAME $LINK_FOLDER
Test_Exit_Status "installing to: ${TOTAL_INSTALL}"

chown -Rv $LOGIN_NAME:$LOGIN_NAME $TOTAL_INSTALL && chown -Rv $LOGIN_NAME:$LOGIN_NAME $LINK_FOLDER$PKG_NAME
Test_Exit_Status "changing ownership of files"

rm -rv /tmp/$TEMP_DIR
echo "Done ${PKG_NAME} installed"


