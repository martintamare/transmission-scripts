#!/bin/bash

LOG_FILE="local0.info"
LOG_APP="finished"
SCRIPT_PATH="/home/torrent/torrent-scripts/"

TORRENT_ID=$1
TORRENT_NAME=$2
TORRENT_PATH=$3

# touch and delete a dummy file to update directory date for apache
# /home/torrent/public/tv/series/season
cd $TORRENT_PATH
# /home/torrent/public/tv/series
cd ..
touch dummy
rm dummy

# log using syslog
logger -p $LOG_FILE -t $LOG_APP "$TORRENT_NAME" 

# calling python script to sort file
"$SCRIPT_PATH"torrent_ended.py "$TORRENT_NAME" $TORRENT_PATH

# sending a prowl notification
"$SCRIPT_PATH"send_prowl.py "$TR_TORRENT_NAME"

# generate rss
"$SCRIPT_PATH"generate_rss.py
