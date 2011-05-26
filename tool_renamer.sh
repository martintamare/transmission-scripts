#!/bin/sh

DIR="/home/torrent/public/tv/the.shield/s7"
cd $DIR

for old in *.avi; do 
	new=`echo $old | sed 's/UNRATED.//' `;
	#echo "old:" + $old + " new:" + $new;
	mv $old $new;
done;
