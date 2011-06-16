#!/bin/sh

LOG_FILE="local0.info"
LOG_APP="flexget"
SCRIPT_PATH="/home/torrent/transmission-scripts/"

# log using syslog
logger -p $LOG_FILE -t $LOG_APP "new torrent: " "$1"