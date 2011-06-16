#!/bin/bash

LOG_FILE="local0.info"
LOG_APP="finish.sh"
SCRIPT_PATH="/home/torrent/transmission-scripts/"

# log using syslog
logger -p $LOG_FILE -t $LOG_APP "New finished torrent, id=$TR_TORRENT_ID name=" "$TR_TORRENT_NAME" 

# calling python script to sort file
"$SCRIPT_PATH"torrent_ended.py "$TR_TORRENT_NAME" $TR_TORRENT_ID

# sending a prowl notification
"$SCRIPT_PATH"send_prowl.py "$TR_TORRENT_NAME"

# generate rss
"$SCRIPT_PATH"generate_rss.py
