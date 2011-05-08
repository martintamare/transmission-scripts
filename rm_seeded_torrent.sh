#!/bin/sh

SCRIPTS_DIR="/home/torrent/transmission-scripts/"

# To do beauty !
. /home/torrent/transmission-scripts/bash-beauty.sh

# file where TR_ADMIN, TR_PASSWORD are stored
. /home/torrent/transmission-scripts/my_password.sh

# script to check for complete torrents in transmission folder, then stop and move them
# get torrent list from transmission-remote list
# delete first / last line of output
# remove leading spaces
# get first field from each line
TORRENTLIST=`transmission-remote -n $TR_ADMIN:$TR_PASSWORD -l | sed -e '1d;$d;s/^ *//' | cut -s -d " " -f1`
LIMIT_RATIO="120"

# for each torrent in the list
for TORRENTID in $TORRENTLIST 
do
	
	# check the ratio
	RATIO=`transmission-remote -n $TR_ADMIN:$TR_PASSWORD --torrent $TORRENTID --info  | grep "Ratio:" | cut -s -d ":" -f2`
	# echo $RATIO
	if [ $RATIO != "None" ]; then
		# printTask -t -w 50 "Ratio non vide"
		# printInfo
	
		# convert it to make comparison
		INT_RATIO=`echo $RATIO '*100' | bc -l | awk -F '.' '{ print $1; exit; }'`
		# echo $INT_RATIO
		
		# check torrent’s current state is “Stopped”, “Finished”, or “Idle”
		STATE_STOPPED=`transmission-remote -n $TR_ADMIN:$TR_PASSWORD --torrent $TORRENTID --info | grep "State: Stopped\|Finished\|Idle"`
		# echo $STATE_STOPPED

		# Store torrent's name
		NAME=`transmission-remote -n $TR_ADMIN:$TR_PASSWORD --torrent $TORRENTID -i | grep "Name:" | cut -s -d ":" -f2`
		# printTask -w 50 "${NAME:1:49}"
		# printOk
	
		# Check seeding time
		SEEDING=`transmission-remote -n $TR_ADMIN:$TR_PASSWORD --torrent $TORRENTID --info | grep "Seeding Time:" | cut -s -d ":" -f2`
		PERIOD=`echo $SEEDING | cut -s -d " " -f2`
		NB_PERIOD=`echo $SEEDING | cut -s -d " " -f1`
		
		
		# printTask -w 50 "Ratio : $RATIO"
		# printOk
	
		# if the torrent is “Stopped”, “Finished”, or “Idle” after seeding 100%…
		if [ $INT_RATIO -ge $LIMIT_RATIO ] && [ "$STATE_STOPPED" != "" ]; then
			echo ""

			printTask -t -w 50 "torrent id $TORRENTID finished"
			printWarn
		
			printTask -w 50 "${NAME:1:49}"
			printInfo
			
			printTask -w 50 "Ratio : $RATIO"
			printInfo
		
			# move the files and remove the torrent from Transmission
			/home/torrent/transmission-scripts/torrent_seeded.py "${NAME:1}"
	
			#printTask -t -w 50 "deleting torrent"
			#printInfo
			/home/torrent/transmission-scripts/rm_torrent.sh $TORRENTID
			
		#If torrent has been seeded for a week, remove it !
		elif [ "$PERIOD" == "days" ] && (( "$NB_PERIOD" >= 7 )); then
			/home/torrent/transmission-scripts/rm_torrent.sh $TORRENTID
		fi
	fi
done