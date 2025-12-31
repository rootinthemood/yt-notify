#!/bin/sh
PKG_NAME="yt-notify"
INSTALL_FOLDER=$HOME"/.local/opt/"
TOTAL_INSTALL=$INSTALL_FOLDER$PKG_NAME
PYTHON_INSERT="os.chdir(\"${TOTAL_INSTALL}/\")"
TEMP_DIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'TEMP_DIR')
DESKTOP_LOCATION="/usr/share/applications/${PKG_NAME}.desktop"

Check_Installed () {
  if ! command -v $1 >/dev/null 2>&1
  then
      echo "$1 could not be found, install $1 first"
      exit 1
  fi
}

Create_Desktop_File () {
echo "[Desktop Entry]
Name=yt-notify
Comment=Follow and track youtube channels without account
Type=Application
Categories=Utility;
Terminal=false
Path=$TOTAL_INSTALL
Exec=uv run ./yt-notify/main.py
Icon=$TOTAL_INSTALL/images/icon.png" | sudo tee $DESKTOP_LOCATION > /dev/null
}

Check_Installed uv
Check_Installed mpv
Check_Installed yt-dlp

printf "This script installs '${PKG_NAME}'\n
it places the files in ${INSTALL_FOLDER}\n
Continue?(y/n): "

while read answer
do
  case $answer in
        yes|y)  break ;;
        no|n)   exit  ;;
        *)
                      ;;
   esac
done

Test_Exit_Status () {
    if [ $? -eq 1 ]
    then
        rm -r $TEMP_DIR
        printf "\nError installing! Problem with: $1\n"
        exit
    fi
}

shopt -s extglob
cp -rv !(setup.sh) $TEMP_DIR && \
cd $TEMP_DIR
Test_Exit_Status "temporary directory in /tmp/"
shopt -u extglob

sed -i "15 i$PYTHON_INSERT" ./yt-nofify/main.py
Test_Exit_Status "sed changing source code"

mkdir -pv $TOTAL_INSTALL && \
cp -rv ./* $TOTAL_INSTALL && \
Test_Exit_Status "installing to: ${TOTAL_INSTALL}"

chown -Rv $USER:$USER $TOTAL_INSTALL
Test_Exit_Status "changing ownership of files"

cd $TOTAL_INSTALL && \
uv sync
Test_Exit_Status "uv syncing dependencies"

Create_Desktop_File
printf "\nCreated .desktop file..."
Test_Exit_Status "creating .desktop file"

rm -r $TEMP_DIR
printf "\nRemoved temporary directory..."
printf "\n\nDone ${PKG_NAME} installed!"
