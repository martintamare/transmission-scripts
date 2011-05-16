#!/bin/sh

LOG_DIR="/home/torrent/log/"
LOG=$LOG_DIR"flexget"

# To do beauty !
. /home/torrent/transmission-scripts/bash-beauty.sh

printTask -t -w 50 "New torrent" >> $LOG
printWarn >> $LOG
printTask -w 50 "${1:0:49}" >> $LOG
printInfo >> $LOG
