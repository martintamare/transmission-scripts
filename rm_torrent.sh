#!/bin/bash

. /home/torrent/transmission-scripts/bash-beauty.sh
. /home/torrent/transmission-scripts/my_password.sh

STATUS=`transmission-remote  -n $TR_ADMIN:$TR_PASSWORD --torrent $1 --remove  | cut -d "\"" -f2` 
#printTask -t -w 50 "$STATUS"
#printOk
