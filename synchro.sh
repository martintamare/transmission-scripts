#!/bin/sh

# Simple rsync "driver" script.  (Uses SSH as the transport layer.)
# http://www.scrounge.org/linux/rsync.html

# Demonstrates how to use rsync to back up a directory tree from a local
# machine to a remote machine.  Then re-run the script, as needed, to keep
# the two machines "in sync."  It only copies new or changed files and ignores
# identical files.

# Destination host machine name
DEST="home"

# User that rsync will connect as
# Are you sure that you want to run as root, though?
USER="martin"

# Directory to copy from on the source machine.
TVDIR="/home/torrent/public/tv"
MOVIEDIR="/home/torrent/public/movies/"

# Directory to copy to on the destination machine.
TVDESTDIR="/home/media/"
MOVIEDESTDIR="/home/media/temp/"

. /home/torrent/transmission-scripts/bash-beauty.sh

# excludes file - Contains wildcard patterns of files to exclude.
# i.e., *~, *.bak, etc.  One "pattern" per line.
# You must create this file.
# EXCLUDES=/root/bin/excludes

# Options.
# -n Don't do any copyi, but display what rsync *would* copy. For testing.
# -a Archive. Mainly propogate file permissions, ownership, timestamp, etc.
# -u Update. Don't copy file if file on destination is newer.
# -v Verbose -vv More verbose. -vvv Even more verbose.
# See man rsync for other options.

# For testing.  Only displays what rsync *would* do and does no actual copying.
#OPTS="-n -u -r -L --rsh=ssh --exclude-from=$EXCLUDES  --log-format=%n"
# Does copy, but still gives a verbose display of what it is doing
OPTS="-u -L -r --rsh=ssh --exclude-from=$EXCLUDES --log-format=%n"
# Copies and does no display at all.
#OPTS="--archive --update --rsh=ssh --exclude-from=$EXCLUDES --quiet"

# May be needed if run by cron?
export PATH=$PATH:/bin:/usr/bin:/usr/local/bin

PROCESS="rsync"
pgrep $PROCESS >/dev/null 
if [ "$?" = "1" ]
then 
	# Only run rsync if $DEST responds.
 	VAR=`ping -s 1 -c 1 $DEST > /dev/null; echo $?`
 	if [ $VAR -eq 0 ] 
	then
		

		TV_DATE=`printTask -t`
		TV_STATUS=`rsync $OPTS $TVDIR $USER@$DEST:$TVDESTDIR 2>&1`
		echo $TV_STATUS >> /home/torrent/log/debug
		TV_STATUS2=`echo $TV_STATUS | sed '/rsync:.*]/d' | sed 's/ /\n/g' | sed s_tv/.*/__ | sed '/^$/d'`
		if [ "$TV_STATUS2" != "" ]; then
			echo ""
			echo -n $TV_DATE
			echo -n " "
			printTask -w 36 "starting rsync on TV"
			printWarn
			echo $TV_STATUS2 | sed 's/ /\n/g'
			printTask -t -w 50 "rsync on TV finished"
			printOk
		fi

		MOVIE_DATE=`printTask -t`
		MOVIE_STATUS=`rsync $OPTS $MOVIEDIR $USER@$DEST:$MOVIEDESTDIR 2>&1 | sed 's/rsync:.*]//' | sed 's/ /\n/g' | sed 's/\(.*[\/]\).*/\1/' | grep "/$"`
		if [ "$MOVIE_STATUS" != "" ]; then
			echo ""
			echo -n $MOVIE_DATE
			echo -n " "
			printTask -w 36 "starting rsync on MOVIES"
			printWarn
			echo $MOVIE_STATUS | sed 's/ /\n/g'
			printTask -t -w 50 "rsync on MOVIES finished"
			printOk
		fi
	fi
fi
