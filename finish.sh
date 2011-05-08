#!/bin/bash

LOG="/home/torrent/log/finish"

. /home/torrent/transmission-scripts/bash-beauty.sh

# Skip first line
echo "" >> $LOG
printTask -t -w 50 "New finished torrent" >> $LOG
printWarn >> $LOG

printTask -t -w 50 "Raw data" >> $LOG
printInfo >> $LOG
#echo "$TR_APP_VERSION $TR_TIME_LOCALTIME $TR_TORRENT_DIR $TR_TORRENT_HASH $TR_TORRENT_ID $TR_TORRENT_NAME" >> $LOG

printTask -w 50 "${TR_TORRENT_NAME:0:49}" >> $LOG
printOk >> $LOG

printTask -w 50 "Id : $TR_TORRENT_ID" >> $LOG
printOk >> $LOG

/home/torrent/transmission-scripts/torrent_ended.py "$TR_TORRENT_NAME" $TR_TORRENT_ID >> $LOG 2>&1

#/home/torrent/scripts/generate_rss.py >> $LOG 2>&1
