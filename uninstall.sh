#!/bin/sh
PKG_NAME="yt-notify"
INSTALL_FOLDER=$HOME"/.local/opt/"
TOTAL_INSTALL=${INSTALL_FOLDER}${PKG_NAME}
DESKTOP_LOCATION=$HOME"/.local/share/applications/${PKG_NAME}.desktop"
ICON_FOLDER=$HOME"/.local/share/icons/"
DATA_FOLDER=$HOME"/.local/share/${PKG_NAME}"
CONFIG_FOLDER=$HOME"/.config/${PKG_NAME}"

Get_Answer () {
  while read answer
    do
      case $answer in
            yes|y)  break ;;
            no|n)   exit  ;;
            *)
                          ;;
       esac
    done
}

printf "This script uninstalls '${PKG_NAME}'\n
It will not delete the data located at '${DATA_FOLDER}' '\n
Continue?(y/n): "

Get_Answer

Test_Exit_Status () {
    if [ $? -eq 1 ]
    then
        printf "\nError! $1\n"
        exit
    fi
}

rm -r $TOTAL_INSTALL
Test_Exit_Status "Removing: ${TOTAL_INSTALL}"

rm -r $DESKTOP_LOCATION
Test_Exit_Status "Removing: ${DESKTOP_LOCATION}"

rm -r "${ICON_FOLDER}yt-notify.ico" "${ICON_FOLDER}yt-notify.png"
Test_Exit_Status "Removing: '${ICON_FOLDER}yt-notify.ico' '${ICON_FOLDER}yt-notify.png'"

rm -r $CONFIG_FOLDER
Test_Exit_Status "Removing: ${CONFIG_FOLDER}"

printf "\n\nDone ${PKG_NAME} uninstalled!\n"

printf "Also delete files at '${DATA_FOLDER}'?\n
Continue?(y/n): "

Get_Answer
rm -r $DATA_FOLDER
Test_Exit_Status "Removing: ${DATA_FOLDER}"
