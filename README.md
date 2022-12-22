# yt-notify
Program that wil help you follow and track youtube channels and its videos without an account. Stores the data in json format. Made with PyQt6 and scrapetube.

![yt-notify01_2](https://user-images.githubusercontent.com/105909072/169989558-b5eb0a02-8e46-4d82-ac0e-2ac865cde0a6.png)

## Requirements
```bash
pip install PyQt6 py-notifier requests scrapetube
```
or
```bash
pip install -r requirements.txt
```


## Run
```bash
git clone https://github.com/rootinthemood/yt-notify.git
cd yt-notify
pip install -r requirements.txt
python3 ./main.py
```

## Install
If you want to install and be able to directly call 'yt-notify' from terminal.
```bash
git clone https://github.com/rootinthemood/yt-notify.git
cd yt-notify
pip install -r requirements.txt
sudo ./setup.sh
```

## Update
Update to a new version? Follow Install again. All your settings will be saved.

Tested on Linux

* Features
    * Add/Remove channel
    * Update channel/All channels
    * Open video in browser
    * Open video in mpv/vlc
    * mpv/VLC argument settings
    * Currently watching
    * Search for videos
