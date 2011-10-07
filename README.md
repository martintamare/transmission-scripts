Collection of various scripts I used to extend transmission
=================

Here is a small explanations of all the scripts. I'll try to update them often, making them better and better !

Last update:
------------
Change log to handle syslog. The local0 file is used !
Change script to use deluge. Why deluge ? Cause with flexget, the ratio and sorting can be automated in a better way ...

To do:
------------
test syslog and improves rsync log (duplicates & stuff)

Description of the scripts:
---------------------------
**create_db.py** - small python script to create local database to store tv shows information (avoiding over-asking tvdb database)

**finish.sh** - called by transmission when a torrent has finish downloading. It starts other scripts

**generate_rss.py** - does what the name is saying ;) Using a local sqlite database to store tv show information (name of the episode)

**log_flexget.sh** - very simple script to log flexget downloads

**rm_seeded_torrent.sh** - script called every hour : check ratio of seeding torrent and remove torrent with a sufficient ratio.

**rm_torrent.sh** - simple script to remove a torrent in transmission using his id

**send_prowl.py** - simple python script to send notification to prowl (growl like system for phone notification)

**synchro.sh** - rsync script to copy data of my local server at home

**tool_renamer.sh** - I always forget how to batch rename file using bash. This tool makes my life easier

**torrent_ended.py** - when a torrent is finished : checks if it's a tv show or not.

- If yes : creates a symlink (to be able to seed) to a sorted directory (tv/tvshowname/seasonnumber/file)

- If no : move to a private section where I will manually (:() move it

**torrent_sended.py** - removes the symlink previously created

**update_blocklist.sh** - script called once a week to update blocklist
